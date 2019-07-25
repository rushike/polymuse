from rmidi import mutils
from rmidi.MIDI import MIDI
from rmidi.absolutemidi import AbsoluteMidi
from rmidi.constant import converter
from rmidi.dataset import config
from rmidi.constant import meta_event_format

import numpy


"""
Pianoroll 

Each track, track in shape[0]

Note number. note in shape[1]

Temporal, time / ticks in shape[2]
        T I M E  
      _________________>  shape[2]
     |
  N  |
  O  |
  T  |
  E  |
    \_/
  shape[1]


More on temporal dimension than of note side

Data prepare assumes 4 measure prev input for note pridiction

Returns:
    [PianoRoll] -- midi pianoroll representation object
"""

class PianoRoll:
    
    def __init__(self, midi, print_threshold = 25):
        self.midi = midi
        self.print_threshold = print_threshold
        self.roll = None
        self.note_range = None
        self.track_range = None
        pass

    def pianoroll(self, note_range = None, track_range = None):
        if not isinstance(self.midi, AbsoluteMidi):
            self.midi = AbsoluteMidi.to_abs_midi(self.midi)
        
        N = 128 if not note_range else note_range[1] - note_range[0] 
        
        self.note_range = [0, 128] if not note_range  else note_range 
        
        self.track_range = [0, self.midi.track_count] if not track_range else track_range if not numpy.isscalar(track_range) else [track_range - 1, track_range]

        LEN = 4800
        trackers = numpy.zeros(self.midi.track_count)
        track_anas = meta_event_format.X
        res_set = numpy.zeros((self.midi.track_count, N, LEN))
        for i in range(self.track_range[0], self.track_range[1]):
            t = self.midi.tracks[i]
            instrument = t.get_event('instrument_name', depth = 1)
            try :
                ttempo = t.get_event('set_tempo', depth = 1)
                tempo = mutils.toint(ttempo[0].data, 8)
                # tempo = ttempo
            except IndexError:
                #Occurs because set_tempo is not register in every track explicitly, usually in first track only and all track follows the same rhythm forward
                #Considering the tempo_event in first track [0] , if there too error raised then tempo == 120 bpm
                try:
                    ttempo = self.midi.tracks[0].get_event('set_tempo', depth = 1)
                    tempo = mutils.toint(ttempo[0].data, 8)
                except IndexError:
                    tempo = 500000
                pass
            nit = 0 #numpy array iterator
            prev_oucr, dut = 0, 0
            # print(t.trk_event[-11 : -1])
            for e in t.trk_event:
                if e.is_note_on_off_event():
                    noteval = e.data[0] - self.note_range[0]
                    if noteval >= N: continue
                    if prev_oucr == e.abstime: 
                        nit -= dut
                    
                    dut = int(32 // mutils.nth_note(e.elength, tempo=tempo)) 
                    prev_oucr = e.abstime
                    res_set[i][noteval][nit: nit + dut] += 1
                    nit += dut
        self.roll = res_set
        return res_set


    def prepare_data(self, ip_memory = 25):
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory

        Assuming the pianoroll return roll with 32th note accuracy, i.e 1 / 32 of whole note   ....... need to confirm
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        notes = self.pianoroll()
        # print(self.to_str())
        data_in, data_out = [], []
        tracks, notes_n, timediv = notes.shape
        for t in range(tracks):
            le = timediv
            chunks_count = le // ip_memory + 1
            for i in range(chunks_count):
                start, end = i * ip_memory , (i + 1) * ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
                buffer = numpy.zeros((128, ip_memory))
                buffer[:, :buf_size] = notes[t][:, start : start + buf_size]
                data_in.append(buffer)
                data_out.append((notes[t, :, end] if end < le else numpy.zeros((128))))

        # print(data_in)
        # print(data_out)
        return numpy.array(data_in), numpy.array(data_out)

    @staticmethod
    def to_midi(pianoroll): 
        """Converts the pianoroll representation to midi object
        
        Arguments:
            pianoroll {[type]} -- [description]
        """
        if type(pianoroll) == PianoRoll: pianoroll = pianoroll.roll
        
        track, notes_n, time_n = pianoroll.shape

        mid = MIDI(track_count = track, empty = False) # Creating the empty MIDI object
        on_note_set = set()
        for t in range(track): # Iteratinf 0th axis, to specific track
            delta_time = 0
            for tim in range(1, time_n): # First iterating the 2 axis before 1nd, due to algo nature
                first_bool = True
                for nt in range(notes_n): #Iterating note axis  
                    if first_bool and pianoroll[t, nt, tim] == 1 and pianoroll[t, nt, tim - 1] == 0: # pushing the first note with delta time == delta_time var, in that time slice which is on in current instance
                        # if nt not in on_note_set:
                        #     on_note_set.add(nt)
                        #     mid.tracks[t].push_note(delta_time, nt, intensity = 0x50)
                        #     pass
                        # else:
                        #     pass
                        mid.tracks[t].push_note(delta_time, nt, channel_no = 0, intensity = 0x50)
                        delta_time = 0 #setting delta time(relative time) to zero
                        first_bool = False
                    elif pianoroll[t, nt, tim] == 1  and pianoroll[t, nt, tim - 1] == 0: # pushing other than first note with deltatime 0
                        mid.tracks[t].push_note(0, nt, channel_no = 0, intensity = 0x50)
                    elif pianoroll[t, nt, tim] == 0 and pianoroll[t, nt, tim - 1] == 1: #closing note trigger, closing the note
                        mid.tracks[t].close_note(0, nt, channel_no = 0)

                    else: #do nothing pass
                        pass

                delta_time += 32 # Incrementing delta count, as if no first note instance played


        pass

        return mid

    def to_str(self, res = None):
        try:
            p_str = ""
            tracks, notes, intervals = numpy.shape(self.roll)
            for t in range(self.track_range[0], self.track_range[1]):
                for n in range(notes):
                    p_str += "%3s : " % mutils.midi_to_note(n + self.note_range[0])
                    for i in  range(self.print_threshold):
                        if self.roll[t][n][i] == 1:
                            # p_str += ("\x1b[0;30;43m %4d \x1b[0m" % self.roll[t][n][i]) 
                            p_str +=  u"\u2589" * 6 # \u2588"
                        else : p_str += (" %4d " % self.roll[t][n][i])#( str(self.roll[t][n][i]) + " -- " )
                    p_str += "\n"

                p_str += "************************ NEW TRACK ***************************************************** NEW TRACK **************************************************************\n"
            return p_str
        except Exception: return None
        
    def __repr__(self):
        try:
            p_str = ""
            tracks, notes, intervals = numpy.shape(self.roll)
            for t in range(self.track_range[0], self.track_range[1]):
                for n in range(notes):
                    p_str += "%3s : " % mutils.midi_to_note(n + self.note_range[0])
                    for i in  range(self.print_threshold):
                        if self.roll[t][n][i] == 1:
                            # p_str += ("\x1b[0;30;43m %4d \x1b[0m" % self.roll[t][n][i]) 
                            p_str +=  u"\u2589" * 6 # \u2588"
                        else : p_str += (" %4d " % self.roll[t][n][i])#( str(self.roll[t][n][i]) + " -- " )
                    p_str += "\n"

                p_str += "************************ NEW TRACK ***************************************************** NEW TRACK **************************************************************\n"
            return p_str
        except Exception: return None

class CPianoRoll:
    def __init__(self, midi, octave, offset = 4, print_threshold = 25):
        self.midi = midi
        self.octave = octave
        self.offset = offset
        self.print_threshold = print_threshold

            

        def cpiano_roll(self):
            pass
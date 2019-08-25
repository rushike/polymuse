from rmidi import mutils
from rmidi.MIDI import MIDI
from rmidi.absolutemidi import AbsoluteMidi
from rmidi.constant import converter
from rmidi.dataset import config
from rmidi.constant import meta_event_format

from polymuse.dataset.constants import ZEROS_FIVE, NOTE_LENGTH 
from polymuse.dataset import dutils 

import numpy, random, copy


"""
Aim : to keep the time track with less redunducy as in piano roll

"""

class Piano_sFlat:
    def __init__(self, midi, print_threshold = 25):
        self.midi = midi
        self.print_threshold = print_threshold
        self.roll = None
        self.note_range = None
        self.track_range = None
        self.__DEPTH__ = 5

    def flat_pianoroll(self, note_range = None, track_range = None, trim = True):
        """min timespan of roll 32nd note
        
        Keyword Arguments:
            note_range {list} -- 2 element list/tuple (default: {None})
            track_range {list} -- 2 element list/tuple (default: {None})
        
        Returns:
            [ndarray] -- flat_piano_roll
        """
        if not isinstance(self.midi, AbsoluteMidi):
            self.midi = AbsoluteMidi.to_abs_midi(self.midi)
        
        N = 128 if not note_range else note_range[1] - note_range[0] 
        
        self.note_range = [0, 128] if not note_range  else note_range 
        
        self.track_range = [0, self.midi.track_count] if not track_range else track_range if not numpy.isscalar(track_range) else [track_range - 1, track_range]

        LEN = 9600
        trackers = numpy.zeros(self.midi.track_count)
        track_anas = meta_event_format.X
        res_set = numpy.zeros((self.midi.track_count, LEN, self.__DEPTH__))
        print(res_set.shape)
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
            dep = -1
            for e in t.trk_event:
                
                if e.is_note_on_off_event():
                    noteval = e.data[0] - self.note_range[0]
                    
                    
                    if prev_oucr == e.abstime : 
                        nit -= dut

                    if prev_oucr == e.abstime or dep == -1:
                        dep += 1 # going to next note on same time instance
                        
                        
                    else :
                        dep = 0
                        # nit += 1 # going to next note instance
                    
                    if noteval >= N : continue
                    if dep >= self.__DEPTH__ : 
                        dep = 0
                        continue
                    dut = int(32 // mutils.nth_note(e.elength, tempo=tempo)) 
                    prev_oucr = e.abstime
                    for k in range(dut):
                        res_set[i][nit + k][dep] = noteval
                    # res_set[i][nit : nit + dut][dep] += noteval 
                    nit += dut
        self.roll = res_set

        if trim:
            res_set_list = []
            for i in range(res_set.shape[0]):
                res_set_trk_list = []
                for n in range(res_set.shape[1]):
                    if numpy.any(res_set[i, n]):
                        res_set_trk_list.append(list(res_set[i][n]))

                res_set_list.append(res_set_trk_list)
            MX = max([len(l) for l in res_set_list])

            return dutils.to_numpy_array_from_3D_list(res_set_list, [res_set.shape[0] , MX, 5])

        return res_set


    def prepare_data(self, ip_memory = 25, stack = True):
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory

        Assuming the pianoroll return roll with 32th note accuracy, i.e 1 / 32 of whole note   ....... need to confirm
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        notes = self.flat_pianoroll()
        # print(self.to_str())
        data_in, data_out = [], []
        tracks, timediv, note_depth = notes.shape
        for t in range(tracks):
            le = timediv
            chunks_count = le // ip_memory + 1
            data_in.append([])
            data_out.append([])
            for i in range(chunks_count):
                start, end = i * ip_memory , (i + 1) * ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
                buffer = numpy.zeros((ip_memory, self.__DEPTH__))
                buffer[:buf_size, :] = notes[t][start : start + buf_size, :]
                data_in[t].append(buffer)
                data_out[t].append((notes[t, end, :] if end < le else numpy.zeros((self.__DEPTH__))))

        # print(data_in)
        # print(data_out)
        
        return numpy.array(data_in), numpy.array(data_out)

    @staticmethod
    def to_midi(roll, depth = 5): 
        """Converts the pianoroll representation to midi object
        
        Arguments:
            pianoroll {[type]} -- [description]
        """
        # raise NotImplementedError("piano_sflat.to_midi not implemented yet.")
        if type(roll) == Piano_sFlat: roll = roll.roll
        print(roll.shape)
        useless, time_n, track, notes_n, = roll.shape
        roll = roll[0]
        mid = MIDI(track_count = track, empty = False) # Creating the empty MIDI object
        # on_note_set = set()
        # for t in range(track): # Iteratinf 0th axis, to specific track
        #     delta_time = 0
        #     for tim in range(1, time_n): # First iterating the 2 axis before 1nd, due to algo nature
        #         first_bool = True
        #         for nt in range(notes_n): #Iterating note axis  
        #             noteval = int(roll[tim, t, nt])
        #             if first_bool and roll[tim, t, nt] != 0 and roll[ tim - 1, t, nt] == 0: # pushing the first note with delta time == delta_time var, in that time slice which is on in current instance
                        
        #                 mid.tracks[t].push_note(delta_time, noteval, channel_no = 0, intensity = 0x50)
        #                 delta_time = 0 #setting delta time(relative time) to zero
        #                 first_bool = False
        #             elif roll[tim, t, nt] != 0  and roll[tim - 1, t, nt] == 0: # pushing other than first note with deltatime 0
        #                 mid.tracks[t].push_note(0, noteval, channel_no = 0, intensity = 0x50)
        #             elif roll[tim, t, nt] == 0 and roll[tim - 1, t, nt] != 0: #closing note trigger, closing the note
        #                 mid.tracks[t].close_note(0, noteval, channel_no = 0)

        #             else: #do nothing pass
        #                 pass

        #         delta_time += 32 # Incrementing delta count, as if no first note instance played


        # pass
        for t in range(track):
            del_tm = 0
            # t_spread = copy.copy(roll[0, t, :])
            t_spread = numpy.zeros(notes_n)
            pr_noteval = 0
            for tm in range(time_n - 1):
                for n in range(notes_n) :
                    noteval = int(roll[tm,t,n])
                    ah_noteval = int(roll[tm + 1, t, n])
                    if noteval < 20: continue
                    # if tm > 100: continue
                    # print("... ", t, n, noteval, ah_noteval)
                    # print(t_spread)
                    
                    if noteval == ah_noteval and t_spread[n] == 0: #new ON State
                        # print("pushing ", noteval)
                        mid.tracks[t].push_note(dutils.note_length(del_tm), noteval, 0, 80)
                        t_spread[n] = noteval
                        del_tm = 0
                    elif noteval != ah_noteval and t_spread[n] == noteval: # new OFF State:
                        # print("closing ",dutils.note_length(del_tm), noteval)
                        mid.tracks[t].close_note(dutils.note_length(del_tm), noteval, 0)
                        t_spread[n] = 0
                        del_tm = 0
                    elif noteval == pr_noteval and t_spread[n] == 0:
                        pass
                    elif noteval != pr_noteval and t_spread[n] != 0:
                        pass
                    
                del_tm += 1
            # print("++++++++++++++++++++++++++++============================") 
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

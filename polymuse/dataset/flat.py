from rmidi import mutils
from rmidi.MIDI import MIDI
from rmidi.absolutemidi import AbsoluteMidi
from rmidi.constant import converter
from rmidi.dataset import config
from rmidi.constant import meta_event_format

import numpy


class Flat:

    def __init__(self, midi, print_threshold = 25):
        self.midi = midi
        self.print_threshold = print_threshold
        self.flat = None
        # self.note_range = None
        self.track_range = None
        pass
    
    def flat_notes(self, track_range = None, trim = True):
        
        if not isinstance(self.midi, AbsoluteMidi):
            self.midi = AbsoluteMidi.to_abs_midi(self.midi)
        
        N = 128  
        
        # self.note_range = [0, 128] if not note_range  else note_range 
        
        self.track_range = [0, self.midi.track_count] if not track_range else track_range if not numpy.isscalar(track_range) else [track_range - 1, track_range]

        LEN = 4800
        
        trackers = numpy.zeros(self.midi.track_count)
        track_anas = meta_event_format.X
        res_set = numpy.zeros((self.midi.track_count, LEN))
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
            tp = 0
            for e in t.trk_event:
                if e.is_note_on_off_event():
                    noteval = e.data[0] 
                    res_set[i][tp] = noteval
                    tp += 1 
        # self.flat_roll = res_set
    
        if trim:
            res_set_list = []
            for i in range(res_set.shape[0]):
                res_set_list.append(numpy.trim_zeros(res_set[i], 'b'))
            return res_set_list
        return res_set

    def flat_time(self):

        pass
    
    def flat_roll(self,  track_range = None):
        if not isinstance(self.midi, AbsoluteMidi):
            self.midi = AbsoluteMidi.to_abs_midi(self.midi)
        
        N = 128  
        
        # self.note_range = [0, 128] if not note_range  else note_range 
        
        self.track_range = [0, self.midi.track_count] if not track_range else track_range if not numpy.isscalar(track_range) else [track_range - 1, track_range]

        LEN = 4800
        
        trackers = numpy.zeros(self.midi.track_count)
        track_anas = meta_event_format.X
        res_set = numpy.zeros((self.midi.track_count, LEN))
        for i in range(self.track_range[0], self.track_range[1]):
            t = self.midi.tracks[i]
            instrument = t.get_event('instrument_name', depth = 1)
            try :
                ttempo = t.get_event('set_tempo', depth = 1)
                tempo = mutils.toint(ttempo[0].data, 8)
                # tempo = ttempo
            except IndexError:
                #Occurs because set_tempo is not register in every track explicitly, usually specified in first track only and all track follows the same rhythm forward
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
                    noteval = e.data[0] 
                    if prev_oucr == e.abstime: 
                        nit -= dut
                    
                    dut = int(32 // mutils.nth_note(e.elength, tempo=tempo)) 
                    prev_oucr = e.abstime
                    res_set[i][nit: nit + dut] += noteval 
                    nit += dut
        self.flat_roll = res_set
        return res_set

    def prepare_data(self, ip_memory = 25):
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        notes = self.flat_notes()
        data_in, data_out = [], []
        for t in notes:
            le = len(t)
            chunks_count = le // ip_memory + 1
            for i in range(chunks_count):
                start, end = i * ip_memory , (i + 1) * ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
                buffer = numpy.zeros(ip_memory)
                buffer[:buf_size] = t[start : start + buf_size]
                data_in.append(buffer)
                data_out.append(([t[end]] if end < le else [0]))

        print(data_in)
        print(data_out)
        return numpy.array(data_in), numpy.array(data_out)
        

    def to_str(self, res = None, track_range = None):
        res = res
        track_range = track_range if track_range else self.track_range
        try:
            p_str = ""
            tracks, intervals = numpy.shape(self.flat_roll)
            for t in range(track_range[0], track_range[1]):
                    # p_str += "%3s : " % mutils.midi_to_note(n + self.note_range[0])
                for i in  range(self.print_threshold):
                    # if self.flat_roll[t][i] == 1:
                    #     # p_str += ("\x1b[0;30;43m %4d \x1b[0m" % self.roll[t][n][i]) 
                    #     p_str +=  u"\u2589" * 6 # \u2588"
                    p_str += (" %4d " % self.flat_roll[t][i])#( str(self.roll[t][n][i]) + " -- " )
                p_str += "\n"

                p_str += "************************ NEW TRACK ***************************************************** NEW TRACK **************************************************************\n"
            return p_str
        except Exception: return None        
        
        
    def __repr__(self):
        try:
            p_str = ""
            tracks, intervals = numpy.shape(self.flat_roll)
            for t in range(self.track_range[0], self.track_range[1]):
                    # p_str += "%3s : " % mutils.midi_to_note(n + self.note_range[0])
                for i in  range(self.print_threshold):
                    # if self.flat_roll[t][i] == 1:
                    #     # p_str += ("\x1b[0;30;43m %4d \x1b[0m" % self.roll[t][n][i]) 
                    #     p_str +=  u"\u2589" * 6 # \u2588"
                    p_str += (" %4d " % self.flat_roll[t][i])#( str(self.roll[t][n][i]) + " -- " )
                p_str += "\n"

                p_str += "************************ NEW TRACK ***************************************************** NEW TRACK **************************************************************\n"
            return p_str
        except Exception: return None
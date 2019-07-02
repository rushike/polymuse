from rmidi import mutils
from rmidi.MIDI import MIDI
from rmidi.absolutemidi import AbsoluteMidi
from rmidi.constant import converter
from rmidi.dataset import config
from rmidi.constant import meta_event_format

import numpy


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
            

         
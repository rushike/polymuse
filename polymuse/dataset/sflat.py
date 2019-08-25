


from rmidi import mutils
from rmidi.MIDI import MIDI
from rmidi.absolutemidi import AbsoluteMidi
from rmidi.constant import converter
from rmidi.dataset import config
from rmidi.constant import meta_event_format

from polymuse.dataset.constants import ZEROS_FIVE, NOTE_LENGTH 
from polymuse.dataset import dutils

import numpy, random


"""
Five note representation
** Assumes a track can contian max 5 notes

Note 0      int
Note 1      int
Note 2      int
Note 3      int
Note 4      int

Note 5      int

Note are filled from 0 -> 4 fassion


Returns:
    [sFlat] -- sFlat object
"""

class sFlat():
    __DEPTH__ = 5
    __SPREAD__ = 8
    __TIME_LEN__ = 1
    __TSPREAD__ = 6
    def __init__(self, midi, print_threshold = 25):
        self.midi = midi
        self.print_threshold = print_threshold
        self.roll = None
        # self.note_range = None
        self.__DEPTH__ = sFlat.__DEPTH__
        self.track_range = None
        pass
    
    def flat_notes(self, track_range = None, trim = True, note_range = None):
        
        if not isinstance(self.midi, AbsoluteMidi):
            self.midi = AbsoluteMidi.to_abs_midi(self.midi)
        
        N = 128  
        
        self.note_range = [0, 128] if not note_range  else note_range 
        
        self.track_range = [0, self.midi.track_count] if not track_range else track_range if not numpy.isscalar(track_range) else [track_range - 1, track_range]

        LEN = 10000
        
        trackers = numpy.zeros(self.midi.track_count)
        track_anas = meta_event_format.X
        res_set = numpy.zeros((self.midi.track_count, LEN, self.__DEPTH__))
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
            # tp = 0
            # for e in t.trk_event:
            #     if e.is_note_on_off_event():
            #         noteval = e.data[0] 
            #         res_set[i][tp] = noteval
            #         tp += 1 
            """
            >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            """
            nit = 0 #numpy array iterator
            prev_oucr, dut, dep  = -1, 0, 0
            dep = 0
            for e in t.trk_event:
                
                if e.is_note_on_off_event():
                    # if e.is_note_off_event(): continue
                    if 0x8f < e.event_id < 0x90 or e.data[1] == 0: continue
                    noteval = e.data[0] 
                    # res_set[i][tp] = noteval
                    # tp += 1 
                    #builting from here
                    if prev_oucr == e.abstime: 
                        dep += 1 # going to next note on same time instance
                    else :
                        dep = 0
                        nit += 1 # going to next note instance

                    noteval = e.data[0] - self.note_range[0]
                    if noteval >= N or dep >= self.__DEPTH__: continue
                    
                    
                    dut = int(32 // mutils.nth_note(e.elength, tempo=tempo)) if mutils.nth_note(e.elength, tempo=tempo) != 0 else 0
                    prev_oucr = e.abstime
                    res_set[i][nit][dep] += noteval
                    # nit += dut

        self.roll = res_set
    
        if trim:
            res_set_list = []
            for i in range(res_set.shape[0]):
                booln = False
                res_set_trk_list = []
                for n in range(res_set.shape[1]):
                    if numpy.array_equal(res_set[i][n], ZEROS_FIVE) and booln: continue
                    # res_nt = [0, 0, 0, 0, 0]
                    # for j in range(res_set.shape[2]):
                    #     res_nt[j] = res_set[i][n][j]
                    res_set_trk_list.append(list(res_set[i][n]))
                    booln = True
                res_set_list.append(res_set_trk_list)
            MX = max([len(l) for l in res_set_list])
            # print(res_set_list)
            return dutils.to_numpy_array_from_3D_list(res_set_list, [res_set.shape[0] , MX, 5])
        return res_set


    def flat_time(self, track_range = None, trim = True, note_range = None):
        if not isinstance(self.midi, AbsoluteMidi):
            self.midi = AbsoluteMidi.to_abs_midi(self.midi)
        
        N = 128  
        
        self.note_range = [0, 128] if not note_range  else note_range 
        
        self.track_range = [0, self.midi.track_count] if not track_range else track_range if not numpy.isscalar(track_range) else [track_range - 1, track_range]

        LEN = 10000
        
        trackers = numpy.zeros(self.midi.track_count)
        track_anas = meta_event_format.X
        res_set = numpy.zeros((self.midi.track_count, LEN, 1))
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

            """
            >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            """
            nit = 0 #numpy array iterator
            prev_oucr, dut, dep  = -1, 0, 0
            dep = 0
            for e in t.trk_event:
                
                if e.is_note_on_off_event():
                    # if e.is_note_off_event(): continue
                    if 0x8f < e.event_id < 0x90 or e.data[1] == 0: continue
                    noteval = e.data[0] 

                    #builting from here
                    if prev_oucr == e.abstime: 
                        dep += 1 # going to next note on same time instance
                    else :
                        dep = 0
                        nit += 1 # going to next note instance

                    noteval = e.data[0] - self.note_range[0]
                    if noteval >= N or dep >= self.__DEPTH__: continue
                    
                    
                    dut = int(32 // mutils.nth_note(e.elength, tempo=tempo)) if mutils.nth_note(e.elength, tempo=tempo) != 0 else 0
                    prev_oucr = e.abstime
                    res_set[i][nit][0] = dut


        self.time = res_set
    
        if trim:
            res_set_list = []
            for i in range(res_set.shape[0]):
                booln = False
                res_set_trk_list = []
                for n in range(res_set.shape[1]):
                    if numpy.array_equal(res_set[i][n], [0]) and booln: continue
                    
                    res_set_trk_list.append(list(res_set[i][n]))
                    booln = True
                res_set_list.append(res_set_trk_list)
            MX = max([len(l) for l in res_set_list])
            # print(res_set_list)
            return dutils.to_numpy_array_from_3D_list(res_set_list, [res_set.shape[0] , MX, 1])
        return res_set

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

    def prepare_data(self, notes, track_range = None, ip_memory = 25):
        return sFlat.prepare_data(self.flat_notes())
    @staticmethod
    def prepare_data(notes, track_range = None, ip_memory = 25):
<<<<<<< HEAD
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        track_range = track_range if track_range else [0, 1]
        # notes = self.flat_notes() if notes == None else notes
        data_in, data_out = [], []
        for tr in range(track_range[1] - track_range[0]):
            # trk = tr - track_range[0]
            nt = notes[tr]
            data_in.append([])
            data_out.append([])
            lent = len(notes[tr])
            # for j in range(lent):
            le = len(nt)
            
            chunks_count = le // ip_memory + 1
            # for i in range(chunks_count):                #two consecutive chunks have no notes common, two line in group
            #     start, end = i * ip_memory , (i + 1) * ip_memory
            for i in range(le - ip_memory):
                start, end = i, i + ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
                buffer = numpy.zeros((ip_memory, sFlat.__DEPTH__))
                buffer[:buf_size, :] = nt[start : start + buf_size]
                data_in[tr].append(buffer)
                # print(t[end])
                data_out[tr].append((nt[end] if end < le else notes[0][0]))
        
        if track_range[1]- track_range[0] == 1: #is scalar, no track
            data_in, data_out = data_in[0], data_out[0]
        return numpy.array(data_in), numpy.array(data_out)
        
    @staticmethod
    def prepare_data_3D(notes, track_range = None, ip_memory = 25):
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        track_range = track_range if track_range else [0, 1]
        print("SHHHHHHHHHHSHSHSHHSHHS L ", notes.shape)
        # notes = self.flat_notes() if notes == None else notes
        data_in, data_out = [], []
        for tr in range(track_range[1] - track_range[0]):
            # trk = tr - track_range[0]
            nt = notes[tr]
            data_in.append([])
            data_out.append([])
            lent = len(notes[tr])
            # for j in range(lent):
            le = len(nt)
                
            chunks_count = le // ip_memory + 1
            # for i in range(chunks_count):                #two consecutive chunks have no notes common, two line in group
            #     start, end = i * ip_memory , (i + 1) * ip_memory
            for i in range(le - ip_memory):
                start, end = i, i + ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
                buffer = numpy.zeros((ip_memory, sFlat.__DEPTH__, sFlat.__SPREAD__))
                buffer[:buf_size, :] = nt[start : start + buf_size]
                data_in[tr].append(buffer)
                # print(t[end])
                data_out[tr].append((nt[end] if end < le else notes[0][0]))
            
        if track_range[1]- track_range[0] == 1: #is scalar, no track
            data_in, data_out = data_in[0], data_out[0]
        return numpy.array(data_in), numpy.array(data_out)

    @staticmethod
    def prepare_data_time(notes, track_range = None, ip_memory = 25):
=======
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        track_range = track_range if track_range else [0, 1]
<<<<<<< HEAD
        print("time ", notes.shape)
=======
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543
        # notes = self.flat_notes() if notes == None else notes
        data_in, data_out = [], []
        for tr in range(track_range[1] - track_range[0]):
            # trk = tr - track_range[0]
            nt = notes[tr]
            data_in.append([])
            data_out.append([])
            lent = len(notes[tr])
            # for j in range(lent):
            le = len(nt)
<<<<<<< HEAD
                
=======
            
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543
            chunks_count = le // ip_memory + 1
            # for i in range(chunks_count):                #two consecutive chunks have no notes common, two line in group
            #     start, end = i * ip_memory , (i + 1) * ip_memory
            for i in range(le - ip_memory):
                start, end = i, i + ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
<<<<<<< HEAD
                buffer = numpy.zeros((ip_memory, sFlat.__TIME_LEN__, sFlat.__TSPREAD__))
=======
                buffer = numpy.zeros((ip_memory, sFlat.__DEPTH__))
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543
                buffer[:buf_size, :] = nt[start : start + buf_size]
                data_in[tr].append(buffer)
                # print(t[end])
                data_out[tr].append((nt[end] if end < le else notes[0][0]))
<<<<<<< HEAD
            
=======
        
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543
        if track_range[1]- track_range[0] == 1: #is scalar, no track
            data_in, data_out = data_in[0], data_out[0]
        return numpy.array(data_in), numpy.array(data_out)
        
    @staticmethod
<<<<<<< HEAD
=======
    def prepare_data_3D(notes, track_range = None, ip_memory = 25):
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        track_range = track_range if track_range else [0, 1]
        print("SHHHHHHHHHHSHSHSHHSHHS L ", notes.shape)
        # notes = self.flat_notes() if notes == None else notes
        data_in, data_out = [], []
        for tr in range(track_range[1] - track_range[0]):
            # trk = tr - track_range[0]
            nt = notes[tr]
            data_in.append([])
            data_out.append([])
            lent = len(notes[tr])
            # for j in range(lent):
            le = len(nt)
                
            chunks_count = le // ip_memory + 1
            # for i in range(chunks_count):                #two consecutive chunks have no notes common, two line in group
            #     start, end = i * ip_memory , (i + 1) * ip_memory
            for i in range(le - ip_memory):
                start, end = i, i + ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
                buffer = numpy.zeros((ip_memory, sFlat.__DEPTH__, sFlat.__SPREAD__))
                buffer[:buf_size, :] = nt[start : start + buf_size]
                data_in[tr].append(buffer)
                # print(t[end])
                data_out[tr].append((nt[end] if end < le else notes[0][0]))
            
        if track_range[1]- track_range[0] == 1: #is scalar, no track
            data_in, data_out = data_in[0], data_out[0]
        return numpy.array(data_in), numpy.array(data_out)

    @staticmethod
    def prepare_data_time(notes, track_range = None, ip_memory = 25):
        """Prepares data for the network(RNN) in ip/op format. Here called data_in, data_out.
        With so callled vocab_size of ip_memory
        
        Keyword Arguments:
            ip_memory {int} -- memory or ipsize used in predicting next (default: {25})
        """
        track_range = track_range if track_range else [0, 1]
        print("time ", notes.shape)
        # notes = self.flat_notes() if notes == None else notes
        data_in, data_out = [], []
        for tr in range(track_range[1] - track_range[0]):
            # trk = tr - track_range[0]
            nt = notes[tr]
            data_in.append([])
            data_out.append([])
            lent = len(notes[tr])
            # for j in range(lent):
            le = len(nt)
                
            chunks_count = le // ip_memory + 1
            # for i in range(chunks_count):                #two consecutive chunks have no notes common, two line in group
            #     start, end = i * ip_memory , (i + 1) * ip_memory
            for i in range(le - ip_memory):
                start, end = i, i + ip_memory
                buf_size = ip_memory if end < le else le -  start # only reason due to logic below else not needed
                buffer = numpy.zeros((ip_memory, sFlat.__TIME_LEN__, sFlat.__TSPREAD__))
                buffer[:buf_size, :] = nt[start : start + buf_size]
                data_in[tr].append(buffer)
                # print(t[end])
                data_out[tr].append((nt[end] if end < le else notes[0][0]))
            
        if track_range[1]- track_range[0] == 1: #is scalar, no track
            data_in, data_out = data_in[0], data_out[0]
        return numpy.array(data_in), numpy.array(data_out)
        
    @staticmethod
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543
    def to_midi(sflatroll, time_ins = 0): 
        """Converts the pianoroll representation to midi object
        
        Arguments:
            sflatroll {ndarray} -- sflat ndarray format as describe above
        """
        if type(sflatroll) == sFlat: sflatroll = sflatroll.roll
        
        track, time_n, notes_depth = sflatroll.shape

        mid = MIDI(track_count = track, empty = False) # Creating the empty MIDI object
        on_note_set = set()
        for t in range(track): # Iteratinf 0th axis, to specific track
            delta_time = 0
            for tim in range(1, time_n): # First iterating the 2 axis before 1nd, due to algo nature
                first_bool = True
                n_length = random.choice(NOTE_LENGTH) if not numpy.isscalar(time_ins) else time_ins[tim]
                for nt in range(notes_depth): #Iterating on note axis and pushing the event 
                    noteval = int(sflatroll[t][tim][nt])
                    if noteval == 0: break
                    mid.tracks[t].push_note(0, noteval)
                    # n_length = 0
                    # if first_bool and sflatroll[t, nt, tim] == 1 and sflatroll[t, nt, tim - 1] == 0: # pushing the first note with delta time == delta_time var, in that time slice which is on in current instance
                        
                    #     mid.tracks[t].push_note(delta_time, nt, channel_no = 0, intensity = 0x50)
                    #     delta_time = 0 #setting delta time(relative time) to zero
                    #     first_bool = False
                    # elif pianoroll[t, nt, tim] == 1  and pianoroll[t, nt, tim - 1] == 0: # pushing other than first note with deltatime 0
                    #     mid.tracks[t].push_note(0, nt, channel_no = 0, intensity = 0x50)
                    # elif pianoroll[t, nt, tim] == 0 and pianoroll[t, nt, tim - 1] == 1: #closing note trigger, closing the note
                    #     mid.tracks[t].close_note(0, nt, channel_no = 0)

                    # else: #do nothing pass
                    #     pass

                for nt in range(notes_depth): #Iterating on note axis and closing the event 
                    noteval = int(sflatroll[t][tim][nt])
                    if noteval == 0: break
                    mid.tracks[t].close_note(n_length, noteval, 0)
                    n_length = 0
                
                # delta_time += 32 # Incrementing delta count, as if no first note instance played


        pass

        return mid



    def to_str(self, res = None, track_range = None):
        res = res if res != 0 else self.roll
        track_range = track_range if track_range else self.track_range
        try:
            p_str = ""
            tracks, intervals, depth = numpy.shape(res)
            for t in range(track_range[0], track_range[1]):
                    # p_str += "%3s : " % mutils.midi_to_note(n + self.note_range[0])
                for i in  range(self.print_threshold):
                    # if self.flat_roll[t][i] == 1:
                    #     # p_str += ("\x1b[0;30;43m %4d \x1b[0m" % self.roll[t][n][i]) 
                    #     p_str +=  u"\u2589" * 6 # \u2588"
                    p_str += ("  " + str(res[t][:][i]))#( str(self.roll[t][n][i]) + " -- " )
                p_str += "\n"

                p_str += "************************ NEW TRACK ***************************************************** NEW TRACK **************************************************************\n"
            return p_str
        except NotImplementedError: return None        
        
        
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
                    p_str += (" %4d " % self.flat_roll[t][:][i])#( str(self.roll[t][n][i]) + " -- " )
                p_str += "\n"

                p_str += "************************ NEW TRACK ***************************************************** NEW TRACK **************************************************************\n"
            return p_str
        except Exception: return None


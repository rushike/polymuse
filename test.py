# import rmidi.mutils
from rmidi.MIDI import MIDI
from rmidi import mutils
from polymuse.dataset import piano_roll
import polymuse.net.rnn
import numpy, random

'''
MIDI Object Testinh
'''

import os

print(MIDI)

y = MIDI.parse_midi('./midis/Believer_-_Imagine_Dragons.mid')

tr = y.track(0)

no = tr.notes()



y.compress('check')

# y.create_file('check')

e = mutils.file_hash('./midis/Believer_-_Imagine_Dragons.mid')

d = mutils.file_hash('check.mid')

print(e, ", ", d , " : ", e == d)


'''
Sequence
'''
# mu = rmidi.Muse()
# le = 7
# x = numpy.arange(12, 12 + le, 2)
# se = [1, 2, 4, 8, 16, 32]
# x = [random.choice(se) for i in range(le)]
# y = mu.sequence(le)
# m = mu.muse(x, y)
# print(m)


# m.create_file("test_add_event_ch")
# m.compress("test_add_event_ch")
# c = m.parse_midi('test-legit.mid')
# print(c)
# # c.create_file('duplicate')
# c.compress()


"""
midi_to_note testing from mutuls 
21 -> c0
60 -> c4
"""
# y = mutils.midi_to_note([56, 56, 78, 98, 34, 54, 95])

# y2 = mutils.midi_to_note(60)

# y == y2

"""
Testing the set_tempo of MIDI
"""

# x = MIDI.parse_midi('default.mid')

# x.set_tempo(56)

# x.compress('tempo_change')

'''
nth note
'''
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi)    
# m = AbsoluteMidi.to_abs_midi(mid)
# print(m.tempo)
# t = mutils.nth_note(19.98905, m.tempo)

'''
piano roll testing
'''
fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
mid = MIDI.parse_midi(fi) 
numpy.set_printoptions(threshold=200)

roll = piano_roll.PianoRoll(mid)

roll_mat = roll.pianoroll(note_range=[48, 72], track_range = 1)
st = roll.to_str()
print(st)
print(roll_mat.shape)
1 == 0

# import rmidi.mutils
from rmidi.MIDI import MIDI
from rmidi import mutils
from polymuse.dataset import piano_roll, constants
from polymuse.dataset import flat, sflat, piano_sflat
# from polymuse.player import rnn_player

# from sklearn.model_selection import train_test_split

# from polymuse.deep_net import rnn
# import polymuse.net.rnn
import numpy, random, sys

'''
MIDI Object Testinh
'''

# import os

# print(MIDI)

# y = MIDI.parse_midi('./midis/Believer_-_Imagine_Dragons.mid')

# tr = y.track(0)

# no = tr.notes()



# y.compress('check')

# # y.create_file('check')

# e = mutils.file_hash('./midis/Believer_-_Imagine_Dragons.mid')

# d = mutils.file_hash('check.mid')

# print(e, ", ", d , " : ", e == d)


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
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=200)

# roll = piano_roll.PianoRoll(mid)

# roll_mat = roll.pianoroll(note_range=[48, 72], track_range = 1)
# st = roll.to_str()
# print(st)
# print(roll_mat.shape)

'''
flat roll, notes, time testing
'''
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=200)
# roll = flat.Flat(mid, print_threshold = 2000)

# roll_mat = roll.flat_notes()
# st = roll.to_str()
# print(roll_mat)
# print(roll_mat.shape)


"""

sFlat Roll : Build

"""
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# # numpy.set_printoptions(threshold=200)

# roll =  sflat.sFlat(mid, print_threshold = 1125)

# res = roll.flat_notes()

# mx = 0
# ct = 0
# for vs in res[1]:
#     for j in range(5):
#         if vs[j] != 0:
#             ct += 1
#         else:
#             mx = mx if ct < mx else ct
#             ct = 0
#             break



# print(roll.to_str(res, track_range = [1, 2]))
# print(mx)

"""
Data preparation
"""
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=200)
# roll = sflat.sFlat(mid, print_threshold = 20)

# x, y = roll.prepare_data()

# print(x, "-------------------------------------------------------\n", y)

# print(x.shape, y.shape)

"""
built a demo model, working on
"""
fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
mid = MIDI.parse_midi(fi) 
numpy.set_printoptions(threshold=50)
# print(roll.to_str())
# roll = flat.Flat(mid, print_threshold = 2000)
roll = piano_sflat.Piano_sFlat(mid, print_threshold=25)

roll_mat = roll.flat_pianoroll()
# st = roll.to_str()
# print(st)
# pt = roll_mat[:, :50]
print(roll_mat)
print(roll_mat.shape)
# x, y = roll.prepare_data()


# # x, xte, y, yte = train_test_split(x, y, test_size = 0.01, random_state = 97)

# # x, y = x / 128, y /128

# print(x, y)
# # # print(numpy.shape(pt))
# # print(roll_mat.shape)
# print(x.shape, y.shape)
# # st = "["
# # for tm in range(25):
# #     st += "[" 
# #     for n in range(128):
# #         if x[8][n][tm] == 1 :
# #              st += "-----, "
# #              continue

# #         st += (str(x[8][n][tm]) + ", ")
# #     st += "],\n"
# # st += "]"

# # print(st)
# # model_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\\gpu_m s_flat_init__b_30_e_500" #model path
# # inp = [constants.believer_start]
# # inp = numpy.array(inp)
# # # print(inp)
# epochs = 200
# batch_size = 20
# dropout = 0.5
# cell_count = 512
# model = rnn.built_demo_flat_model(x, y, 's_flat_',cell_count = cell_count, epochs = epochs, batch_size = batch_size, dropout = dropout)

# # p = rnn.predict(model_path, inp)

# res = rnn_player.play(x[0] , model, predict_instances = 1000)
# res = res * 128 
# # print(res)
# # print(res.shape)

# # mid = piano_roll.PianoRoll.to_midi(res)
# mid = sflat.sFlat.to_midi(res)



# mid.create_file("test_nyn_ex_" + cell_count + "_e_"  + str(epochs) + "_b " + str(batch_size) + "_d_"+ str(dropout) + ".mid")
# # 



1 == 0


"""NOTE e = 200, b = 10, d = 1.0 ......... very bad results
"""
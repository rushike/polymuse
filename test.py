# import rmidi.mutils
from rmidi.MIDI import MIDI
from rmidi import mutils
from polymuse.dataset import piano_roll, constants
from polymuse.dataset import flat, sflat, piano_sflat, dutils
from polymuse.player import rnn_player
from polymuse.dataset import flat, sflat, piano_sflat
# from polymuse.player import rnn_player

# from sklearn.model_selection import train_test_split

# from polymuse.deep_net import rnn
# import polymuse.net.rnn
import numpy, random, sys

# from sklearn.model_selection import train_test_split

from polymuse.deep_net import rnn
# import polymuse.net.rnn
import polymuse.dataset.differentiator as delv
import polymuse.dataset.integrate as intg
import numpy, random, sys, json
import matplotlib.pyplot as plt
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

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543

"""
Dataset making
"""

# fi = ['F:\\rushikesh\\project\\dataset\\lakh_dataset\\AlbertHammond\\ItNeverRainsInSouthernCalifornia.1.mid', '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid', 'F:\\rushikesh\\project\dataset\\lakh_dataset\\B.W.Stevenson\\My_Maria.mid' ]

# fi = ['..\\dataset\\midi_gen\\dataset.mid']

# arr = []
# for i, f in enumerate(fi):
#     print(i)
#     mid = MIDI.parse_midi(f)
#     roll = sflat.sFlat(mid, print_threshold = 2000)
#     # roll = piano_sflat.Piano_sFlat(mid, print_threshold=25)
#     roll_mat = roll.flat_notes()
#     arr.extend(list(roll_mat[0]))

# arr = numpy.array(arr)

# print(arr, arr.shape)

# numpy.save('F:\\rushikesh\\project\\polymuse\\midis\\datset_3', arr)

<<<<<<< HEAD
=======
"""
built a demo model, working on
"""
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=1000)

# roll = sflat.sFlat(mid, print_threshold = 2000)

# roll_mat = roll.flat_notes()

# dataset = numpy.load('F:\\rushikesh\\project\\polymuse\\midis\\datset_3.npy')

# dataset = numpy.array([dataset])

# dataset = dutils.to_3D_bin(dataset, 8)
# print(dataset.shape)
# dataset = dataset[:, :, : 1]
# sflat.sFlat.__DEPTH__ = 1


# x, y = sflat.sFlat.prepare_data_3D(notes = dataset, ip_memory = 100)

# print(x.shape, y.shape)

# model_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\\gpu_ex_512_m_one_note_100___b_30_e_50_d_0.3.h5" #model path

# epochs = 50

# batch_size = 30
# dropout = 0.3
# cell_count = 512

# model_name = 'one_note_100_'



# # model = rnn.built_demo_flat_model(x, y, model_name,cell_count = cell_count, epochs = epochs, batch_size = batch_size, dropout = dropout)
# # model = rnn.time_model_sFlat(x, y, model_name, cell_count = cell_count, epochs = epochs, batch_size = batch_size, dropout = dropout)
# model = rnn.load(model_path)

# res = rnn_player.rsingle_play(x[0] , model, y, predict_instances = 1000)



# res = numpy.round(res)

# res = dutils.rev_bin_3D(res, 8)

# print(res.shape)
# numpy.save('roll.np', res)

# mid = sflat.sFlat.to_midi(res)
# y = res[0, :, 0]
# le = numpy.trim_zeros(y).shape[0]

# print(mid.track_count)

# mid.create_file(model_name + "2_ex_" + str(cell_count) + "_e_"  + str(epochs) + "_b " + str(batch_size) + "_d_"+ str(dropout) + ".mid")
# # # 



# 1 == 0

"""NOTE e = 200, b = 10, d = 1.0 ......... very bad results

"""


"""
Built model for time : 
"""

fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
mid = MIDI.parse_midi(fi) 
numpy.set_printoptions(threshold=1000)

roll = sflat.sFlat(mid, print_threshold = 2000)

roll_mat = roll.flat_time()
xn = roll.flat_notes()
# dataset = numpy.load('F:\\rushikesh\\project\\polymuse\\midis\\datset_3.npy')
dataset = roll_mat
# dataset = numpy.array([dataset])

# dataset = dutils.to_3D_bin(dataset, 6)
sflat.sFlat.__TSPREAD__ = 64
dataset = dutils.one_hot(dataset, sflat.sFlat.__TSPREAD__)
xn = dutils.to_3D_bin(xn, 8)
print(dataset[0, : 3])
print(dataset.shape)
dataset = dataset[:, :, :1]
xn = xn[:, :, :1]
xn = numpy.zeros(xn.shape)

sflat.sFlat.__DEPTH__ = 1


x, y = sflat.sFlat.prepare_data_time(notes = dataset, ip_memory = 50)
x_notes, y_notes = sflat.sFlat.prepare_data_3D(notes = xn, ip_memory = 100)
# print(x,'\n', y)
print(x.shape, y.shape)

model_notes_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\\gpu_ex_512_m_one_note_100___b_30_e_50_d_0.3.h5" #model path
model_time_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\gpu_time_512_m_one_time_one_hot_100_adam___b_30_e_50_d_0.3.h5"
epochs = 50

batch_size = 30
dropout = 0.3
cell_count = 512

model_name = 'one_time_one_hot_100_adam_'

# model_path = './polymuse/deep_net/history/gpu_time_' +  str(cell_count) + '_m_' + model_name +'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout)  + ".h5"

# model = rnn.time_model_sFlat(x, y, model_name, cell_count = cell_count, epochs = epochs, batch_size = batch_size, dropout = dropout)

model_notes_path = rnn.load(model_notes_path)
# model_time_path = model
model_time_path = rnn.load(model_time_path)

res_notes, res_time = rnn_player.rsingle_note_time_play(x_notes[0], x[0], model_notes_path, model_time_path, y_notes, y, predict_instances = 300)

print("OUT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print("time_output shape : ", res_time.shape)
res_notes = dutils.rev_bin_3D(res_notes, 8)
# res_notes = numpy.reshape(res_notes, res_notes.shape + (1, ))
res_time = dutils.rev_one_hot(res_time)
res_time = numpy.reshape(res_time, res_time.shape[:-1])
print("RES_NOTES SHAPE : ", res_notes.shape)
print("RES_TIME SHAPE : ", res_time.shape)

print('RES NOTES ---------------------------------------------\n', res_notes[0, 95 : 105])

print('RES TIME ---------------------------------------------\n', res_time[0, 95 : 105])

# res = numpy.round(res)

# res = dutils.rev_bin_3D(res, 8)

print(res_notes.shape)
numpy.save('roll.np', [res_notes, res_time])

mid = sflat.sFlat.to_midi(res_notes, res_time)
# y = res[0, :, 0]
# le = numpy.trim_zeros(y).shape[0]

print(mid.track_count)

mid.create_file(model_name + "2_ex_" + str(cell_count) + "_e_"  + str(epochs) + "_b " + str(batch_size) + "_d_"+ str(dropout) + ".mid")
# # # 


"""

one _ hot encoding

"""

# y =  [[[9], [8], [5], [3], [1]],
#      [[1], [8], [1], [1], [1]]]

# yn = dutils.one_hot(y, 10)

# print(yn)

# ynr = dutils.rev_one_hot(yn)

# print(ynr)
=======
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543
"""
built a demo model, working on
"""
# fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
# mid = MIDI.parse_midi(fi) 
# numpy.set_printoptions(threshold=1000)

# roll = sflat.sFlat(mid, print_threshold = 2000)

# roll_mat = roll.flat_notes()

# dataset = numpy.load('F:\\rushikesh\\project\\polymuse\\midis\\datset_3.npy')

# dataset = numpy.array([dataset])

# dataset = dutils.to_3D_bin(dataset, 8)
# print(dataset.shape)
# dataset = dataset[:, :, : 1]
# sflat.sFlat.__DEPTH__ = 1


# x, y = sflat.sFlat.prepare_data_3D(notes = dataset, ip_memory = 100)

# print(x.shape, y.shape)

# model_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\\gpu_ex_512_m_one_note_100___b_30_e_50_d_0.3.h5" #model path

# epochs = 50

# batch_size = 30
# dropout = 0.3
# cell_count = 512

# model_name = 'one_note_100_'



# # model = rnn.built_demo_flat_model(x, y, model_name,cell_count = cell_count, epochs = epochs, batch_size = batch_size, dropout = dropout)
# # model = rnn.time_model_sFlat(x, y, model_name, cell_count = cell_count, epochs = epochs, batch_size = batch_size, dropout = dropout)
# model = rnn.load(model_path)

# res = rnn_player.rsingle_play(x[0] , model, y, predict_instances = 1000)



# res = numpy.round(res)

# res = dutils.rev_bin_3D(res, 8)

# print(res.shape)
# numpy.save('roll.np', res)

# mid = sflat.sFlat.to_midi(res)
# y = res[0, :, 0]
# le = numpy.trim_zeros(y).shape[0]

# print(mid.track_count)

# mid.create_file(model_name + "2_ex_" + str(cell_count) + "_e_"  + str(epochs) + "_b " + str(batch_size) + "_d_"+ str(dropout) + ".mid")
# # # 



# 1 == 0

"""NOTE e = 200, b = 10, d = 1.0 ......... very bad results
<<<<<<< HEAD

"""


"""
Built model for time : 
"""

fi = '..\\dataset\\midi_gen\\Believer_Imagine_Dragons.mid'
mid = MIDI.parse_midi(fi) 
numpy.set_printoptions(threshold=1000)

roll = sflat.sFlat(mid, print_threshold = 2000)

roll_mat = roll.flat_time()
xn = roll.flat_notes()
# dataset = numpy.load('F:\\rushikesh\\project\\polymuse\\midis\\datset_3.npy')
dataset = roll_mat
# dataset = numpy.array([dataset])

# dataset = dutils.to_3D_bin(dataset, 6)
sflat.sFlat.__TSPREAD__ = 64
dataset = dutils.one_hot(dataset, sflat.sFlat.__TSPREAD__)
xn = dutils.to_3D_bin(xn, 8)
print(dataset[0, : 3])
print(dataset.shape)
dataset = dataset[:, :, :1]
xn = xn[:, :, :1]
xn = numpy.zeros(xn.shape)

sflat.sFlat.__DEPTH__ = 1


x, y = sflat.sFlat.prepare_data_time(notes = dataset, ip_memory = 50)
x_notes, y_notes = sflat.sFlat.prepare_data_3D(notes = xn, ip_memory = 100)
# print(x,'\n', y)
print(x.shape, y.shape)

model_notes_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\\gpu_ex_512_m_one_note_100___b_30_e_50_d_0.3.h5" #model path
model_time_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\gpu_time_512_m_one_time_one_hot_100_adam___b_30_e_50_d_0.3.h5"
epochs = 50

batch_size = 30
dropout = 0.3
cell_count = 512

model_name = 'one_time_one_hot_100_adam_'

# model_path = './polymuse/deep_net/history/gpu_time_' +  str(cell_count) + '_m_' + model_name +'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout)  + ".h5"

# model = rnn.time_model_sFlat(x, y, model_name, cell_count = cell_count, epochs = epochs, batch_size = batch_size, dropout = dropout)

model_notes_path = rnn.load(model_notes_path)
# model_time_path = model
model_time_path = rnn.load(model_time_path)

res_notes, res_time = rnn_player.rsingle_note_time_play(x_notes[0], x[0], model_notes_path, model_time_path, y_notes, y, predict_instances = 300)

print("OUT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print("time_output shape : ", res_time.shape)
res_notes = dutils.rev_bin_3D(res_notes, 8)
# res_notes = numpy.reshape(res_notes, res_notes.shape + (1, ))
res_time = dutils.rev_one_hot(res_time)
res_time = numpy.reshape(res_time, res_time.shape[:-1])
print("RES_NOTES SHAPE : ", res_notes.shape)
print("RES_TIME SHAPE : ", res_time.shape)

print('RES NOTES ---------------------------------------------\n', res_notes[0, 95 : 105])

print('RES TIME ---------------------------------------------\n', res_time[0, 95 : 105])

# res = numpy.round(res)

# res = dutils.rev_bin_3D(res, 8)

print(res_notes.shape)
numpy.save('roll.np', [res_notes, res_time])

mid = sflat.sFlat.to_midi(res_notes, res_time)
# y = res[0, :, 0]
# le = numpy.trim_zeros(y).shape[0]

print(mid.track_count)

mid.create_file(model_name + "2_ex_" + str(cell_count) + "_e_"  + str(epochs) + "_b " + str(batch_size) + "_d_"+ str(dropout) + ".mid")
# # # 


"""

one _ hot encoding

"""

# y =  [[[9], [8], [5], [3], [1]],
#      [[1], [8], [1], [1], [1]]]

# yn = dutils.one_hot(y, 10)

# print(yn)

# ynr = dutils.rev_one_hot(yn)

# print(ynr)
=======
"""
>>>>>>> 99b8fa35ad113cfeb9dbac32493668e19806f20d
>>>>>>> 8f3effa5b00e12eb9a6d4c5b56078eea8c4cc543

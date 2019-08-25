from polymuse.dataset import constants

from polymuse.deep_net import rnn

from polymuse.dataset import dutils

import numpy

def r1_play(ini_ip = None, predict_instances = 250):
    model_path = "F:\\rushikesh\\project\\polymuse\\polymuse\\deep_net\\history\\gpu_model_rnn_sample_1_batch_15_epochs_100"
    model = rnn.load(model_path)
    inp = numpy.array([constants.believer_start])
    res = numpy.zeros((1, 128, predict_instances))

    res[0, :, :25] = inp #initiating the start

    for tm in range(26, predict_instances):
        y = rnn.predict(model, inp)
        y = numpy.round(y)
        print(tm, " y_pred : ", y.shape)
        res[0, : , tm] = y[0]
        shift(inp)
        add(inp, y)
        pass
    return res

def rspread_play(ini_ip, model_path, predict_instances = 250): #(25, 5) shape play
    model = rnn.load(model_path) if type(model_path) == str else model_path
    # inp = numpy.array([constants.believer_start])
    inp = numpy.array([ini_ip])
    shape = [1, predict_instances]
    shape.extend(inp.shape[2:])
    mem = inp.shape[1]
    print("SHAPE --- ", shape)
    res = numpy.zeros(shape)

    res[0, :mem, :, :] = inp #initiating the start

    for tm in range(mem + 1, predict_instances):
        y = rnn.predict(model, inp)
        if 0 < tm < 50 : print("y---", y)
        # y = numpy.round(y)
        # print(tm, " y_pred : ", y.shape)
        res[0, tm, :] = y[0]
        inp = shift(inp, axis= 1)
        add_flatroll(inp, y)
        # print("inp : ", inp)
        
        pass
    return res


def rsingle_play(ini_ip, model_path, yo = None, predict_instances = 250): #(25, 5) shape play
    model = rnn.load(model_path) if type(model_path) == str else model_path
    # inp = numpy.array([constants.believer_start])
    inp = numpy.array([ini_ip])
    shape = [1, predict_instances]
    shape.extend(inp.shape[2:])
    mem = inp.shape[1]
    print("SHAPE --- ", shape)
    res = numpy.zeros(shape)

    res[0, :mem, :] = inp #initiating the start

    for tm in range(mem + 1, predict_instances):
        # print("loop", tm)
        y = rnn.predict_b(model, inp)
        
        if 95 < tm < 150 :
            print("y-00000----- ", yo[tm])
            print("y---", y)
            print("th --", dutils.thresholding(y, 0.1))
        y = dutils.thresholding(y, 0.1)
        # y = numpy.round(y)
        # print(tm, " y_pred : ", y.shape)
        res[0, tm, :] = y[0]
        inp = shift(inp, axis= 1)
        add_flatroll(inp, y)
        # print("inp : ", inp)
        
        pass
    return res





def play(ini_ip, model_path, predict_instances = 250): #(25, 3, 5) shape play
    model = rnn.load(model_path) if type(model_path) == str else model_path
    # inp = numpy.array([constants.believer_start])
    ip_memory = 125
    inp = numpy.array([ini_ip])
    res = numpy.zeros((1, predict_instances, 3, 5))
    print(inp)
    res[0, :ip_memory, :, :] = inp #initiating the start

    for tm in range(26, predict_instances):
        y = rnn.predict(model, inp)
        # y = y * 537
        if tm < 28 : 
            print("y---", y)
            print("ini-- ", inp)
            print("_________________________________________________")
        # y = numpy.round(y)
        # print(tm, " y_pred : ", y.shape)
        res[0, tm, :] = y[0]
        inp = shift(inp, axis= 1)
        add_flatroll(inp, y)
        # print("inp : ", inp)
        
        pass
    return res

def rsingle_note_time_play(ini_ip, ini_ip_tm, model_note, model_time, y_expected_note = None, y_expected_time = None, ip_memory = None, predict_instances = 250):
    model_note = rnn.load(model_note) if type(model_note) == str else model_note
    model_time = rnn.load(model_time) if type(model_time) == str else model_time
    
    ip_memory = ip_memory if ip_memory else ini_ip.shape[0]

    inp = numpy.array([ini_ip])
    inp_tm = numpy.array([ini_ip_tm])
    print("inp time shape : ", inp_tm.shape)
    notes_shape = [1, predict_instances]
    time_shape = [1, predict_instances]
    notes_shape.extend(inp.shape[2:])
    time_shape.extend(inp_tm.shape[2:])
    
    mem = inp.shape[1]
    
    notes = numpy.zeros(notes_shape)
    time = numpy.zeros(time_shape)
    notes[0, :mem, :] = inp #initiating the start

    for tm in range(mem + 1, predict_instances):
        # print("loop", tm)
        y = rnn.predict_b(model_note, inp)
        t_len = rnn.predict_b(model_time, inp_tm)
        if 95 < tm < 150 :
            print("y-00000----- ", y_expected_time[tm])
            print("y---", t_len)
            print("th --", dutils.thresholding(t_len, 0.15))
        y = dutils.thresholding(y, 0.15)
        
        notes[0, tm, :] = y[0]

        time[0, tm, :] = t_len[0]

        inp = shift(inp, axis= 1)
        add_flatroll(inp, y)
        
        inp_tm = shift(inp_tm, axis=1)
        add_flatroll(inp_tm, t_len)
        # print("inp : ", inp)
        
        pass
    return notes, time




def shift(x,  off = 1, axis = 2):
    return numpy.roll(x, -1 * off, axis)

def add_pianoroll(x, y, axis = 2):
    if x.shape[1] != y.shape[1]: raise AttributeError("x[c, : , d] or x.shape[1], and y.shape[0] should be same. ") 
    x[0, :, -1] = y[0]

def add_flatroll(x, y, axis = 2):
    if x.shape[2] != y.shape[1]: raise AttributeError("x[c, d , :] or x.shape[2], and y.shape[1] should be same. ") 
    x[0, -1, :] = y[0]


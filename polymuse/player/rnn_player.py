from polymuse.dataset import constants

from polymuse.deep_net import rnn

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

def play(ini_ip, model_path, predict_instances = 250):
    model = rnn.load(model_path) if type(model_path) == str else model_path
    # inp = numpy.array([constants.believer_start])
    inp = numpy.array([ini_ip])
    res = numpy.zeros((1, predict_instances, 5))

    res[0, :25, :] = inp #initiating the start

    for tm in range(26, predict_instances):
        y = rnn.predict(model, inp)
        # print("y---", y)
        # y = numpy.round(y)
        # print(tm, " y_pred : ", y.shape)
        res[0, tm, :] = y[0]
        inp = shift(inp, axis= 1)
        add_flatroll(inp, y)
        # print("inp : ", inp)
        
        pass
    return res


def shift(x,  off = 1, axis = 2):
    return numpy.roll(x, -1 * off, axis)

def add_pianoroll(x, y, axis = 2):
    if x.shape[1] != y.shape[1]: raise AttributeError("x[c, : , d] or x.shape[1], and y.shape[0] should be same. ") 
    x[0, :, -1] = y[0]

def add_flatroll(x, y, axis = 2):
    if x.shape[2] != y.shape[1]: raise AttributeError("x[c, d , :] or x.shape[2], and y.shape[1] should be same. ") 
    x[0, -1, :] = y[0]


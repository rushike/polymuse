from polymuse.dataset import constants

from polymuse.deep_net import rnn

import numpy

def play(ini_ip = None, predict_instances = 250):
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
def shift(x,  off = 1, axis = 2):
    return numpy.roll(x, off, axis)

def add(x, y, axis = 2):
    if x.shape[1] != y.shape[1]: raise AttributeError("x[c, : , d] or x.shape[1], and y.shape[0] should be same. ") 
    x[0, :, -1] = y[0]
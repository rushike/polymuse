from rmidi.mutils import *
import numpy

def find(dictn, value, depth = 0):
    for k, v in dictn:
        if v == value:
            return dictn
        elif hasattr(v, 'items'): # indicates if dictionary
            return find(v, value, depth - 1)
        else : raise ValueError("Value not found in the nested dictionary")

def note_length(note_len, resolution = 32):
    return resolution / note_len

def to_numpy_array_from_3D_list(listn, shape = [3, le, 5], depth = 1):
    # if depth == 0:
    # le = len(listn)
    res = numpy.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                res[i, j , k] = listn[i][j][k]

    return ress
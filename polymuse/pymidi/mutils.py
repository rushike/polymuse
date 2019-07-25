from rmidi.mutils import *


def find(dictn, value, depth = 0):
    for k, v in dictn:
        if v == value:
            return dictn
        elif hasattr(v, 'items'): # indicates if dictionary
            return find(v, value, depth - 1)
        else : raise ValueError("Value not found in the nested dictionary")
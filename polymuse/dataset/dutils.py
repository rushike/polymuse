import numpy, copy

def to_numpy_array_from_3D_list(listn, shape = [3, 1000, 5], depth = 1):
    # if depth == 0:
    # le = len(listn)
    print(shape)
    res = numpy.zeros(shape)
    for i in range(shape[0]):
        le = len(listn[i])
        for j in range(shape[1]):
            if j >= le: break
            for k in range(shape[2]):    
                res[i, j , k] = listn[i][j][k]

    return res


def note_length(note_len, resolution = 32):
    if note_len == 0: return 0 
    return resolution // note_len

def translate_01_axis(roll, sw_axis = [0, 1]): #translate 1 axis to zeros one, (n, m, ...)   <--->  (m, n, ...)
    # ax_1, ax_2 = sw_axis[0], sw_axis[1]
    # shp = list(roll.shape)
    # shp[ax_1], shp[ax_2] = roll.shape[ax_2], roll.shape[ax_1]
    # n_roll = numpy.zeros(shp)
    return numpy.swapaxes(roll, sw_axis[0], sw_axis[1])
    # for i in range(shp[ax_1]):
    #     for j in range(shp[ax_2]):
    #         n_roll[i][j] = roll[j][i]
    #     pass 
    # pass
    # return n_roll

# def to_bin(arr, spread = 8):
#     mx_axis = len(arr.shape)
#     arrl = []
#     for i in range(arr.shape[0]):
#         if mx_axis >= 1:
#             if mx_axis == 1: arrl[i] = bin_arr(arr[i], spread)
#         else : continue
#         arrl[i].append([])
#         for j in range(arr.shape[1]):
#             if mx_axis >= 2: 
#                 if mx_axis == 2: arrl[i][j] = bin_arr(arr[i, j], spread)
#             else : continue
#             arrl[i][j].append([])
#             for k in range(arr.shape[2]):
#                 if mx_axis >= 3: 
#                     if mx_axis == 3: arrl[i][j][k] = bin_arr(arr[i, j, k], spread)
#                 else : continue
#                 arrl[i][j][k].append([])
#                 for l in range(arr.shape[3]):
#                     if mx_axis >= 4: 
#                         if mx_axis == 4: arrl[i][j][k][l] = bin_arr(arr[i,  j, k, l], spread)
#                     else : continue
#                     arrl[i][j][k][l].append([])
#                     for m in range(arr.shape[4]):
#                         if mx_axis >= 5:
#                             if mx_axis == 5: arrl[i][j][k][l][m] = bin_arr(arr[i, j, k, l, m], spread)
#                         else : continue
#                         arrl[i][j][k][l][m].append([])
#                         for n in range(arr.shape[5]):
#                             if mx_axis >= 6: 
#                                 if mx_axis == 6: arrl[i][j][k][l][m][n] = bin_arr(arr[i, j, k, l, m, n], spread)
#                             else : continue
#                             # arrl[i][j][k][l][m][n].

#     return numpy.array(arrl)

def to_3D_bin(arr, spread):
    res_shape = list(arr.shape)
    arr = numpy.array(arr, dtype = 'int32')
    res_shape.extend([spread])
    print(res_shape)
    res = numpy.zeros(res_shape)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(arr.shape[2]):
                # print("num to pass : ", arr[i][j][k])
                res[i, j, k] = bin_arr(arr[i, j, k], spread)

    return res
    

def rev_bin_3D(arr, spread):
    # arr = numpy.array(arr, dtype = 'int32')
    # res_shape.extend([spread])
    # print("arr -> jklu :", arr.shape[:-1])
    res = numpy.zeros(arr.shape[:-1])
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(arr.shape[2]):
                # print("num to pass : ", arr[i][j][k])
                res[i, j, k] = rev_bin_arr(arr[i, j, k], spread)
    # print(res.shape)
    return res



def rev_bin_arr(ar, spread):
    num = 1 << (spread - 1)
    # print(num)
    res = 0
    for i in range(spread):
        res += (ar[i] * num)
        num //= 2
    return res

def bin_arr(num, spread):
    stl = bin(num)
    # print("Binart val: ", stl)
    st = stl[2:]
    le = len(st)
    k = spread - le
    i = 0
    bin_ar = numpy.zeros(spread, dtype = 'int32')
    for i in range(le):
        bin_ar[i + k] = int(st[i])
    # print(bin_ar)
    return bin_ar


def thresholding(arr, thr):
    arr[arr > thr] = 1
    arr[arr <= thr] = 0
    return arr
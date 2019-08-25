import numpy, copy

def first_integrate(roll_mat, height = [60, 0, 0, 0, 0], axis = 1):
    """
    find the derivative of number numpy ndarray
    """

    res_set = numpy.zeros(roll_mat.shape) 
    # res_set[0, 0] += height
    print()
    lock = True
    last = numpy.array(height)
    for j in range(roll_mat.shape[0]):
        for i in range(1, roll_mat.shape[1]):
            # print('---')
            if roll_mat[j, i, 0] == 0: 
                lock = True
                continue
            if roll_mat[j, i , 0] != 0 and lock:
                res_set[j, i - 1] = copy.copy(last)
                lock = False

            # if i < 10: 
            # print("---------------", last)
            
            res_set[j, i]  = last + roll_mat[j, i]
            last = roll_mat[j, i]
    return res_set
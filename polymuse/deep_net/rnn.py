import  numpy, datetime, json
# import keras.backend 
# from keras.model import Sequential
from keras.models import Sequential, load_model
from keras.optimizers import SGD
from keras.layers import LSTM, Dropout, Dense, Activation, CuDNNLSTM, TimeDistributed, Flatten
from keras.callbacks import ModelCheckpoint
# import polymuse.dataset.flat as flatter

def get_model():
    model = Sequential()
    model.add(LSTM(
        256,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(256))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(100))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')



def built_demo_flat_model(x, y, model_name, IP = None, OP = None, cell_count = 256, epochs = 200, batch_size = 25, dropout = .5 ):
    ip_memory = x.shape[1]
    # print(x)
    # print(y)
    
    IP = x.shape if not IP else IP
    OP = y.shape if not OP else OP

    x = x.reshape(IP[0], IP[1], -1)
    y = y.reshape(OP[0], -1)
    
    IP = x.shape if not IP else IP
    OP = y.shape if not OP else OP

    print("IP: ", IP)
    print("OP: ", OP)
    model = Sequential()
    # model.add(TimeDistributed(Flatten(input_shape=IP[1:])))
    model.add(CuDNNLSTM(cell_count, return_sequences=True, input_shape=(IP[1], numpy.prod(IP[2:]))))
    model.add(Dropout(dropout))

    model.add(CuDNNLSTM(cell_count, return_sequences=True))
    model.add(Dropout(dropout))

    model.add(CuDNNLSTM(cell_count, return_sequences=True))
    model.add(Dropout(dropout))

    # model.add(CuDNNLSTM(cell_count, return_sequences=True))
    # model.add(Dropout(dropout))

    # model.add(CuDNNLSTM(cell_count, return_sequences=True))
    # model.add(Dropout(dropout))

    model.add(CuDNNLSTM(cell_count, return_sequences=False))
    model.add(Dense(cell_count // 2))
    model.add(Dropout(dropout))

    # model.add(CuDNNLSTM(cell_count, return_sequences=False))
    # model.add(Dropout(dropout))
    
    model.add(Dense(numpy.prod(IP[2:])))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    # batch_size = 30 if not batch_size else batch_size
    # epochs = 500 if not epochs else epochs
    
    history = model.fit(x, y, validation_split = 0.1, batch_size=batch_size,  nb_epoch=epochs)
    print("history keys : " , history.history.keys())
    model.save('./polymuse/deep_net/history/gpu_ex_' +  str(cell_count) + '_m_' + model_name +'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout)  + ".h5")
    # numpy.save('./polymuse/deep_net/history/gpu_h_ex' + str(cell_count)+ '_m_' + model_name+'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout) + ".hist", history.history )
    
    # f = './polymuse/deep_net/history/gpu_h_ex' + str(cell_count)+ '_m_' + model_name+'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout) + ".hist"
    f = './polymuse/hist/gpu_h_ex' + str(cell_count)+ '_m_' + model_name+'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout) + ".json"
    with open(f, 'w') as json_file:
        json.dump(history.history, json_file)
    1 == 0
    return model

def load(model):
    if type(model) == str: return load_model(model)

def predict(model, x):
    IP = x.shape
    # print(x.shape)
    sh = [1]
    sh.extend(x.shape[2:])
    x = x.reshape(IP[0], IP[1], -1)
    y = model.predict(x, verbose = 0)
    y = y.reshape(sh)
    return y 


def predict_b(model, x):
    IP = x.shape
    # print(x.shape)
    sh = [1]
    sh.extend(x.shape[2:])
    x = x.reshape(IP[0], IP[1], -1)
    y = model.predict_on_batch(x)
    y = y.reshape(sh)
    return y 



def time_model_sFlat(x, y, model_name, IP = None, OP = None, cell_count = 256, epochs = 200, batch_size = 25, dropout = .5):
    ip_memory = x.shape[1]
    # print(x)
    # print(y)
    
    IP = x.shape if not IP else IP
    OP = y.shape if not OP else OP

    x = x.reshape(IP[0], IP[1], -1)
    y = y.reshape(OP[0], -1)
    
    IP = x.shape if not IP else IP
    OP = y.shape if not OP else OP

    print("IP: ", IP)
    print("OP: ", OP)
    model = Sequential()
    
    model.add(CuDNNLSTM(cell_count, return_sequences=True, input_shape=(IP[1], numpy.prod(IP[2:]))))
    # model.add(Dense(cell_count))
    model.add(Dropout(dropout))

    # model.add(CuDNNLSTM(cell_count, return_sequences=True))
    # model.add(Dense(cell_count))
    # model.add(Dropout(dropout))

    # model.add(CuDNNLSTM(cell_count, return_sequences=True))
    # model.add(Dense(cell_count))
    # model.add(Dropout(dropout))

    

    model.add(CuDNNLSTM(cell_count, return_sequences=True))
    model.add(Dense(cell_count // 2))
    model.add(Dropout(dropout))

    model.add(CuDNNLSTM(cell_count, return_sequences=False))
    model.add(Dense(cell_count // 2))
    model.add(Dropout(dropout))
    
    model.add(Dense(numpy.prod(IP[2:])))
    model.add(Activation('softmax'))

    opt = SGD(lr=0.01, momentum=0.9)

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=[ 'acc'])
    # model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    # batch_size = 30 if not batch_size else batch_size
    # epochs = 500 if not epochs else epochs
 
    filepath = './polymuse/deep_net/history/gpu_time_' +  str(cell_count) + '_m_' + model_name +'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout)  + ".h5"

    checkpoint = ModelCheckpoint(
        filepath, monitor='loss', 
        verbose=0,        
        save_best_only=True,        
        mode='min'
    )    
    callbacks_list = [checkpoint]
    
    history = model.fit(x, y, validation_split = 0.5, shuffle = True,batch_size=batch_size,  nb_epoch=epochs, callbacks = callbacks_list)
    
    print("history keys : " , history.history.keys())
    
    model.save(filepath)
    # numpy.save('./polymuse/deep_net/history/gpu_h_ex' + str(cell_count)+ '_m_' + model_name+'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout) + ".hist", history.history )
    
    # f = './polymuse/deep_net/history/gpu_h_ex' + str(cell_count)+ '_m_' + model_name+'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout) + ".hist"
    f = './polymuse/hist/gpu_h_ex' + str(cell_count)+ '_m_' + model_name+'__b_' + str(batch_size) + "_e_"+str(epochs) + "_d_" + str(dropout) + ".json"
    with open(f, 'w') as json_file:
        json.dump(history.history, json_file)
    1 == 0
    return model

    """
    REPORT
    If validation split is increase from 0.1 to 0.3 , the validation loss , and validation accuracy increase to 0.17 - 0.20 
    If cut out dense layer before dropout, in middle layer validation loss, accuracy  remains same , but loss while training was high 
    If increase the one more layer, and dense layer after LSTM than dropout, then there is no as such change but need to experiment more to get clear value. But Validation is not increaseing as such
    Everything above just made things nonssense, no learning

    One ohot encoding to 64 classes not worked

    Trying adam loss function

    Mean Sqaure Err worked i think

    
    """
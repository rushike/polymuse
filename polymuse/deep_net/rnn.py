import  numpy, datetime
# import keras.backend 
# from keras.model import Sequential
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dropout, Dense, Activation, CuDNNLSTM
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


def built_demo_model(x, y):

    ip_memory = x.shape[1]
    print(x)
    print(y)
    model = Sequential()
    model.add(CuDNNLSTM(128, return_sequences=True, input_shape=(x.shape[1:])))
    model.add(Dropout(0.2))
    model.add(CuDNNLSTM(128, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(128))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    batch_size = 30
    epochs = 500
    history = model.fit(x, y, batch_size=batch_size, nb_epoch=epochs)
    model.save('./polymuse/deep_net/history/gpu_model_rnn_sample_1_batch_' + str(batch_size) + "_epochs_"+str(epochs))
    numpy.save('./polymuse/deep_net/history/gpu_history_rnn_sample_1__batch_' + str(batch_size) + "_epochs_"+str(epochs), history.history)
    1 == 0
    return model

def load(model):
    if type(model) == str: return load_model(model)

def predict(model, x):
    
    # print(x.shape)
    return model.predict(x, verbose = 0) 
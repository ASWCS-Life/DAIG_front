from os import truncate
import h5py
import requests
import tensorflow as tf

import tensorflow.keras as keras

import numpy as np

from tempfile import TemporaryFile

import time

base_url = 'http://118.67.130.33:8000'
# base_url = 'http://127.0.0.1:8000'

temporary_project_id = '60926f7933f0b035a0591d1d'
auth_temp = '98dbaa34-63d1-4400-93f0-c19d019d1d71'


class CustomCallback(tf.keras.callbacks.Callback):
    stop_learning_tok = False

    def on_train_batch_end(self, batch, logs=None):
        if(self.stop_learning_tok):
            self.model.stop_training = True
        else:
            self.model.stop_training = False

callback = CustomCallback()

def stop_learning_internal():
    callback.stop_learning_tok = True

def start_learning_internal():
    callback.stop_learning_tok = False


# 학습 모델 받아오기 (현재 더미 데이터 추후 S3)
def get_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Conv2D(32, (3, 3)),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Dropout(0.25),

        tf.keras.layers.Conv2D(64, (3, 3), padding='same'),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Conv2D(64, (3, 3)),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Dropout(0.25),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10),
        tf.keras.layers.Activation('softmax')
    ])

    opt = tf.keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)
    model.compile(loss='categorical_crossentropy',
                    optimizer=opt,
                    metrics=['accuracy'])

    return model

# 학습 데이터 받아오기 (현재 더미 데이터 추후 S3)
def get_train_data():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    x_train = x_train.astype('float32') / 256
    x_test = x_test.astype('float32') / 256

    y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
    
    return (x_train, y_train), (x_test, y_test)


(x_train, y_train), (x_test, y_test) = get_train_data()

if __name__ == '__main__':
    #model = tf.keras.models.load_model('model.h5')
    #result = np.load("result_70.npy",allow_pickle=True)

    #x_train = np.asarray(np.load('train_data.npy',allow_pickle=True)).astype(np.float32)
    #y_train = np.asarray(np.load('train_label.npy',allow_pickle=True)).astype(np.float32)

    task_num = 50

    data_split=np.split(x_train,task_num)
    label_split=np.split(y_train,task_num)

    model = get_model()

    k = 5

    weight_list = []

    for i in range(0,k):
        weight_list.append(model.get_weights())

    tmp_weight_1 = model.get_weights()
    tmp_weight_2 = model.get_weights()
    tmp_weight_3 = model.get_weights()
    tmp_weight_4 = model.get_weights()
    tmp_weight_5 = model.get_weights()

    epoch = 100

    for index in range(0,10):
        print('step is...',index)
        if(index == 0):
            init_weight = model.get_weights()
        else:
            init_weight = np.array(weight_list[0],dtype = object)

            for i in range(1,k):
                init_weight = init_weight + np.array(weight_list[i],dtype = object)

            init_weight = init_weight/k
            init_weight = init_weight.tolist()
        
        model.set_weights(init_weight)
        model.evaluate(x_test, y_test)

        for i in range(0,k):
            model.set_weights(init_weight)
            model.fit(data_split[index*5+i], label_split[index*5+i], batch_size=32, validation_split=0.2, epochs=epoch, callbacks=[callback], verbose=0)
            weight_list[i] = model.get_weights()

        

    final_weight = np.array(weight_list[0],dtype = object)
    for i in range(1,k):
        final_weight = final_weight + np.array(weight_list[i],dtype = object)

    final_weight = final_weight/k
    final_weight = final_weight.tolist()

    model.set_weights(final_weight)
    model.evaluate(x_test, y_test)
    #model.summary()


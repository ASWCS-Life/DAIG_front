import requests
import json

import tensorflow as tf

from tensorflow.keras import datasets, layers, models

import numpy as np

from .auth import get_auth_header, set_auth_header
from tempfile import TemporaryFile

from sklearn.model_selection import train_test_split

import time

base_url = 'http://127.0.0.1:8000'

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


# rest api

# Login
def login_req(data=None):
    res = requests.post(f'{base_url}/auth/login/', data=data)

    if res.status_code not in [200, 201, 204]:
        raise SystemExit(requests.exceptions.HTTPError)
    return res.json()


# SignUp
def sign_up_req(data=None):
    res = requests.post(f'{base_url}/auth/signup/', data=data, headers=get_auth_header())

    if res.status_code not in [200, 201, 204]:
        raise SystemExit(requests.exceptions.HTTPError)
    return res.json()

def create_project(initial_weight,data=None):
    with TemporaryFile() as tf:
        np.save(tf, np.array(initial_weight,dtype=object))
        _ = tf.seek(0)
        res = requests.post(f'{base_url}/project/create/', files={'weight':tf},data=data, headers={'AUTH':get_auth_header()})

    return res.json()

def get_avaiable_project(params=None):
    res = requests.get(f'{base_url}/project/get/project', params=params, headers={'AUTH':get_auth_header()})
    print(res.json())
    if(res.json()['is_successful']):
        return res.json()['project_uid']
    else:
        return -1

def model_upload(path, data=None):
    res = requests.post(f'{base_url}/{path}/', json=data, headers=get_auth_header())

    #if res.status_code not in [200, 201, 204]:
    #raise exc.ResponseException(res)
    return res.json()

def get_weight(project_id,params=None):
    res = requests.get(f'{base_url}/project/{project_id}/project/weight', params=params, headers={'AUTH':get_auth_header()})

    with TemporaryFile() as tf:
        tf.write(res.content)
        _ = tf.seek(0)
        weight =np.load(tf,allow_pickle=True)

    return weight

# 학습 시작 요청
def start_learning(project_id, params=None):
    callback.stop_learning_tok = False

    res = requests.get(f'{base_url}/project/{project_id}/task/get', params=params, headers={'AUTH':get_auth_header()})
    res_json = res.json()

    print(res_json)

    if(not(res_json['is_successful'])): return 'FAIL'
    occupy_task(project_id,{'task_index':res_json['task_index']})

    model = get_model()

    init_weight = get_weight(project_id)

    model.set_weights(init_weight.tolist())
    task_index = int(res_json['task_index'])
    task_size = int(50000/res_json['total_task'])

    if(task_index == -1): 
        validate(project_id)
        return 'STOP'

    data = x_train[task_index*task_size:(task_index + 1)*task_size]
    label = y_train[task_index*task_size:(task_index + 1)*task_size]

    start_time = time.time()
    model.fit(data, label, batch_size=32, epochs=30, callbacks=[callback], validation_data=(x_test, y_test), verbose=2)
    spent_time = time.time() - start_time

    if callback.stop_learning_tok:
        return 'STOP'

    with TemporaryFile() as tf:
        np.save(tf, np.array(model.get_weights(),dtype=object) - np.array(init_weight,dtype=object))
        _ = tf.seek(0)
        update_success =  update_learning(project_id = project_id,
            params = {'task_index':res_json['task_index'],'spent_time':spent_time},
            gradient = {'gradient':tf})

    if(not(update_success)): return 'FAIL'

    return 'SUCCESS'

# 학습 Task 선점하기
def occupy_task(project_id, params = None):
    res = requests.post(f'{base_url}/project/{project_id}/task/start/',data=params, headers={'AUTH':get_auth_header()})
    return res.json()['is_successful']

# 학습 결과 전송하기
def update_learning(project_id, gradient, params = None):
    res = requests.post(f'{base_url}/project/{project_id}/task/update/',files = gradient, data=params, headers={'AUTH':get_auth_header()})
    return res.json()['is_successful']

def is_project_finished(project_id, params=None):
    res = requests.get(f'{base_url}/project/{project_id}/result', params=params, headers={'AUTH':get_auth_header()})

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.status_code != 270

# 결과 요청
def result_learning(project_id, params=None):
    res = requests.get(f'{base_url}/project/{project_id}/result', params=params, headers={'AUTH':get_auth_header()})

    with TemporaryFile() as tf:
        tf.write(res.content)
        _ = tf.seek(0)
        weight = np.load(tf,allow_pickle=True)
    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return weight

# 중단 요청
def stop_learning(path, params, data=None):
    res = requests.put(f'{base_url}/{path}', params=params, json=data, headers=get_auth_header())

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.json()

# 진행 상태 요청
def status_req(path, params):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.json()

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
    
    X = np.concatenate((x_train,x_test))
    y = np.concatenate((y_train,y_test))


    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=10000, random_state=714)


    return (x_train, y_train), (x_test, y_test)

def validate(project_id):
    model = get_model()

    weight = result_learning(project_id)
    model.set_weights(weight.tolist())

    test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
    print('result is...')
    print(test_loss, test_acc)

if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = get_train_data()
    
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
 
    initial_weight = get_model().get_weights()
    rrs_url = 'some dummy url'
    model_url = 'some dummy url'

    project_create_result = create_project(initial_weight,data={
        'rrs':rrs_url,
        'model_url':model_url,
        'total_task':50,
        'step_size':10
    })

    temporary_project_id = get_avaiable_project()

    start_time = time.time()
    print('start!')

    while(result_learning(temporary_project_id)):
        start_learning(temporary_project_id,get_auth_header())
        time.sleep(1)
    
    print('total time spent')
    print(time.time()-start_time)

    scores = model.evaluate(x_test, y_test, verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])


(x_train, y_train), (x_test, y_test) = get_train_data()
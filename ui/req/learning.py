import requests
import json

import tensorflow as tf

from tensorflow.keras import datasets, layers, models

import numpy as np

from auth import get_auth_header
from tempfile import TemporaryFile

import time

base_url = 'http://127.0.0.1:8000'

temporary_project_id = '60926f7933f0b035a0591d1d'
auth = '98dbaa34-63d1-4400-93f0-c19d019d1d71'

###########################################################
# Dummy Train Data
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# 픽셀 값을 0~1 사이로 정규화합니다.
train_images, test_images = train_images / 255.0, test_images / 255.0

train_images = np.concatenate((train_images, train_images, train_images, train_images), axis=0)
train_labels = np.concatenate((train_labels, train_labels, train_labels, train_labels), axis=0)
###########################################################

# rest api
def create_project(initial_weight,data=None):
    with TemporaryFile() as tf:
        np.save(tf, np.array(initial_weight,dtype=object))
        _ = tf.seek(0)
        res = requests.post(f'{base_url}/project/create', files={'weight':tf},data=data, headers={'AUTH':auth})

    return res.json()

def get_avaiable_project(params=None):
    res = requests.get(f'{base_url}/project/get/project', params=params, headers={'AUTH':auth})
    return res.json()['project_uid']

def model_upload(path, data=None):
    res = requests.post(f'{base_url}/{path}', json=data, headers=get_auth_header())

    #if res.status_code not in [200, 201, 204]:
    #raise exc.ResponseException(res)
    return res.json()

def get_weight(project_id,params=None):
    res = requests.get(f'{base_url}/project/{project_id}/project/weight', params=params, headers={'AUTH':auth})

    with TemporaryFile() as tf:
        tf.write(res.content)
        _ = tf.seek(0)
        weight =np.load(tf,allow_pickle=True)

    return weight

# 학습 시작 요청
def start_learning(project_id, params=None):
    res = requests.get(f'{base_url}/project/{project_id}/task/get', params=params, headers={'AUTH':auth})
    res_json = res.json()

    if(not(res_json['is_successful'])): return 'FAIL'
    occupy_task(project_id,{'task_index':res_json['task_index']})

    model = get_model()

    init_weight = get_weight(project_id)

    model.set_weights(init_weight.tolist())
    data, label = get_train_data(res_json['task_index'],res_json['total_task'])
    model.fit(data, label, epochs=5)

    with TemporaryFile() as tf:
        np.save(tf, np.array(model.get_weights(),dtype=object))
        _ = tf.seek(0)
        update_success =  update_learning(project_id = project_id,
            params = {'task_index':res_json['task_index']},
            gradient = {'gradient':tf})

    if(not(update_success)): return 'FAIL'

    return 'SUCCESS'

# 학습 Task 선점하기
def occupy_task(project_id, params = None):
    res = requests.post(f'{base_url}/project/{project_id}/task/start',data=params, headers={'AUTH':auth})
    return res.json()['is_successful']

# 학습 결과 전송하기
def update_learning(project_id, gradient, params = None):
    res = requests.post(f'{base_url}/project/{project_id}/task/update',files = gradient, data=params, headers={'AUTH':auth})
    return res.json()['is_successful']

# 결과 요청
def result_learning(project_id, params=None):
    res = requests.get(f'{base_url}/project/{project_id}/result', params=params, headers={'AUTH':auth})

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.status_code == 270

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
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

    return model

# 학습 데이터 받아오기 (현재 더미 데이터 추후 S3)
def get_train_data(task_index, total_task):
    task_size = int(240000/total_task)



    return train_images[task_size*task_index:task_size*(task_index+1)],train_labels[task_size*task_index:task_size*(task_index+1)]

if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    x_train = x_train.astype('float32') / 256
    x_test = x_test.astype('float32') / 256

    # Convert class vectors to binary class matrices.
    y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
    
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
        start_learning(temporary_project_id)
        time.sleep(1)
    
    print('total time spent')
    print(time.time()-start_time)

    scores = model.evaluate(x_test, y_test, verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])

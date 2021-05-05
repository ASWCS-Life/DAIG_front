import requests
import json

import tensorflow as tf

from tensorflow.keras import datasets, layers, models

import numpy as np

from auth import get_auth_header
from tempfile import TemporaryFile

import time

base_url = 'http://118.67.130.33:8000'

temporary_project_id = '60926f7933f0b035a0591d1d'

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
def create_project(path, initial_weight,data=None):
    with TemporaryFile() as tf:
        np.save(tf, np.array(initial_weight,dtype=object))
        _ = tf.seek(0)
        res = requests.post(f'{base_url}/{path}', files={'weight':tf},data=data, headers={'AUTH':'0054cebf-8d04-4fd6-b74b-90f7252720aa'})

    return res.json()

def get_avaiable_project(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers={'AUTH':'0054cebf-8d04-4fd6-b74b-90f7252720aa'})
    print(res.json())

    return res.json()['project_uid']

def model_upload(path, data=None):
    res = requests.post(f'{base_url}/{path}', json=data, headers=get_auth_header())

    #if res.status_code not in [200, 201, 204]:
    #raise exc.ResponseException(res)
    return res.json()

def get_weight(path,params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers={'AUTH':'0054cebf-8d04-4fd6-b74b-90f7252720aa'})

    with TemporaryFile() as tf:
        tf.write(res.content)
        _ = tf.seek(0)
        weight =np.load(tf,allow_pickle=True)

    return weight

# 학습 시작 요청
def start_learning(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers={'AUTH':'0054cebf-8d04-4fd6-b74b-90f7252720aa'})
    res_json = res.json()

    if(not(res_json['is_successful'])): return 'FAIL'

    print(res_json)

    occupy_task('project/'+temporary_project_id+'/task/start',{'task_index':res_json['task_index']})

    model = get_model()

    init_weight = get_weight('project/'+temporary_project_id+'/project/weight')

    model.set_weights(init_weight.tolist())
    data, label = get_train_data(res_json['task_index'],res_json['total_task'])
    model.fit(data, label, epochs=5)

    with TemporaryFile() as tf:
        np.save(tf, np.array(model.get_weights(),dtype=object))
        _ = tf.seek(0)
        update_success =  update_learning(path='project/'+temporary_project_id+'/task/update',
            params={'task_index':res_json['task_index']},
            gradient={'gradient':tf})

    if(not(update_success)): return 'FAIL'

    return 'SUCCESS'

# 학습 Task 선점하기
def occupy_task(path, params = None):
    res = requests.post(f'{base_url}/{path}',data=params, headers={'AUTH':'0054cebf-8d04-4fd6-b74b-90f7252720aa'})
    return res.json()['is_successful']

# 학습 결과 전송하기
def update_learning(path, gradient, params = None):
    res = requests.post(f'{base_url}/{path}',files = gradient, data=params, headers={'AUTH':'0054cebf-8d04-4fd6-b74b-90f7252720aa'})
    return res.json()['is_successful']

# 결과 요청
def result_learning(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.json()

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
    temporary_project_id = get_avaiable_project('project/get/project')

    while(result_learning('project/'+temporary_project_id+'/result')):
        start_learning('project/'+temporary_project_id+'/task/get')
        time.sleep(1)
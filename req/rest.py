import requests

import numpy as np

from auth import get_auth_header
from tempfile import TemporaryFile

base_url = 'http://localhost:8000'

# rest api
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

    print(weight)

    return 

# 학습 시작 요청
def start_learning(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

    model = models.Sequential(layers.Conv2D(16,(3,3), strides = 3, input_shape = (590 , 445, 3)),
        layers.MaxPooling2D(),
        layers.Conv2D(32, (3,3),strides=2),
        layers.MaxPooling2D(),
        layers.Conv2D(64, (3,3)),
        layers.MaxPooling2D(),
        layers.Conv2D(64,(3,3)),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(256, activation = 'relu'),
        layers.Dropout(0.5),
        layers.Dense(9, activation = 'softmax'))

    #if res.status_code not in [200, 201, 204]:
    #raise exc.ResponseException(res)
    return res.json()

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


if __name__ == '__main__':
    get_model('project/609044ce33f0b03da0d57899/project/result')
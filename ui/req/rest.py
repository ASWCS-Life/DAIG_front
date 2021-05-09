import requests
import numpy as np

from .auth import *
from tempfile import TemporaryFile
import json

import tensorflow as tf

from tensorflow.keras import datasets, layers, models

import time

base_url = 'http://127.0.0.1:8000' # local port


# 프로젝트 생성
def create_project(initial_weight, data=None):
    with TemporaryFile() as tf:
        np.save(tf, np.array(initial_weight, dtype=object))
        _ = tf.seek(0)
        res = requests.post(f'{base_url}/project/create', files={'weight': tf}, data=data,
                            headers=get_auth_header()) # get_header
    print(res.json())
    return res.json()

# 프로젝트 아이디 받기
def get_avaiable_project(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())
    return res.json()['project_uid']

# weight 값 받아오기
def get_weight(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers={'AUTH': '0054cebf-8d04-4fd6-b74b-90f7252720aa'})

    with TemporaryFile() as tf:
        tf.write(res.content)
        _ = tf.seek(0)
        weight = np.load(tf, allow_pickle=True)

    return weight


# 학습 시작 요청
'''
def start_learning(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers={'AUTH': '0054cebf-8d04-4fd6-b74b-90f7252720aa'}) # get_header
    res_json = res.json()

    if (not (res_json['is_successful'])): return 'FAIL'
    occupy_task('project/' + temporary_project_id + '/task/start', {'task_index': res_json['task_index']}) #get_pId


    init_weight = get_weight('project/' + temporary_project_id + '/project/weight') #get_pId

    model.set_weights(init_weight.tolist())
    data, label = get_train_data(res_json['task_index'], res_json['total_task'])
    model.fit(data, label, epochs=5)

    with TemporaryFile() as tf:
        np.save(tf, np.array(model.get_weights(), dtype=object))
        _ = tf.seek(0)
        update_success = update_learning(path='project/' + temporary_project_id + '/task/update',
                                         params={'task_index': res_json['task_index']},
                                         gradient={'gradient': tf}) #get_pId

    if (not (update_success)): return 'FAIL'

    return 'SUCCESS'
'''

# 학습 Task 선점하기
def occupy_task(path, params=None):
    res = requests.post(f'{base_url}/{path}', data=params, headers={'AUTH': '0054cebf-8d04-4fd6-b74b-90f7252720aa'}) #get_header
    return res.json()['is_successful']


# 학습 결과 전송하기
def update_learning(path, gradient, params=None):
    res = requests.post(f'{base_url}/{path}', files=gradient, data=params,
                        headers={'AUTH': '0054cebf-8d04-4fd6-b74b-90f7252720aa'}) #get_header
    return res.json()['is_successful']


# 결과 요청
def result_learning(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers={'AUTH': '0054cebf-8d04-4fd6-b74b-90f7252720aa'}) #get_header

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.status_code == 270


# 중단 요청
def stop_learning(path, params, data=None):
    res = requests.put(f'{base_url}/{path}', params=params, json=data, headers=get_auth_header())

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.json()


# 학습 데이터 받아오기 (현재 더미 데이터 추후 S3)
def get_train_data(task_index, total_task):
    task_size = int(240000 / total_task)

    return train_images[task_size * task_index:task_size * (task_index + 1)], train_labels[
                                                                              task_size * task_index:task_size * (
                                                                                          task_index + 1)]


# Login
def login_req(data=None):
    res = requests.post(f'{base_url}/auth/login/', data=data)
    print(base_url)
    if res.status_code not in [200, 201, 204]:
        raise SystemExit(requests.exceptions.HTTPError)
    return res.json()


# SignUp
def sign_up_req(data=None):
    res = requests.post(f'{base_url}/auth/signup', data=data, headers=get_auth_header())
    print(base_url)
    if res.status_code not in [200, 201, 204]:
        raise SystemExit(requests.exceptions.HTTPError)
    return res.json()

'''
if __name__ == '__main__':
    initial_weight = get_model().get_weights() # 이 부분에 대한 작업필요
    rrs_url = 'some dummy url'
    model_url = 'some dummy url'

    project_create_result = create_project('project/create', initial_weight, data={
        'rrs': rrs_url,
        'model_url': model_url,
        'total_task': 30,
        'step_size': 10
    })

    temporary_project_id = get_avaiable_project('project/get/project')

    start_time = time.time()
    print('start!')

    while (result_learning('project/' + temporary_project_id + '/result')):
        start_learning('project/' + temporary_project_id + '/task/get')
        time.sleep(3)

    print('total time spent')
    print(time.time() - start_time)
'''

#########################이전 파일 내용##############################
'''
import requests

from .auth import get_auth_header

base_url = 'http://127.0.0.1:8000'



# get
def get(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

    if res.status_code not in [200, 201, 204]:
        raise SystemExit(requests.exceptions.HTTPError)
    return res.json()


# put(중단 요청)
def stop_learning(path, params, data=None):
    res = requests.put(f'{base_url}/{path}', params=params, json=data, headers=get_auth_header())

    if res.status_code not in [200, 201, 204]:
        raise SystemExit(requests.exceptions.HTTPError)
    return res.json()
'''


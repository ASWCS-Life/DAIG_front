from os import truncate
from typing import Type
import h5py
import requests
import tensorflow as tf
from .alert import response_alert
import tensorflow.keras as keras

import numpy as np

from .auth import get_auth_header
from tempfile import TemporaryFile

import time

base_url = 'http://118.67.130.33:8000'
#base_url = 'http://127.0.0.1:8000'

class CustomCallback(tf.keras.callbacks.Callback): 
    stop_learning_tok = False

    def on_train_batch_end(self, batch, logs = None): 
        if(self.stop_learning_tok): 
            self.model.stop_training = True
        else : 
            self.model.stop_training = False

callback = CustomCallback()

def stop_learning_internal(): 
    callback.stop_learning_tok = True

def start_learning_internal(): 
    callback.stop_learning_tok = False


# rest api

# Login
def login_req(data = None): 
    res = requests.post(f'{base_url}/auth/login/', data = data)

    response_alert(res.status_code)
    return res.json()


# SignUp
def sign_up_req(data = None): 
    res = requests.post(f'{base_url}/auth/signup/', data = data)

    response_alert(res.status_code)
    return res.json()

def create_project(initial_weight,data = None): 
    with TemporaryFile() as tf : 
        np.save(tf, np.array(initial_weight,dtype = object))
        _ = tf.seek(0)
        res = requests.post(f'{base_url}/project/create/', files = {'weight' : tf},data = data, headers = {'AUTH' : get_auth_header()})
        response_alert(res.status_code)

    return res.json()

def get_avaiable_project(params = None): 
    res = requests.get(f'{base_url}/project/get/project', params = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    print(res.json())
    if(res.json()['is_successful']): 
        return res.json()['project_uid']
    else : 
        return -1

def upload_data(data_path, label_path, project_uid, task_num): 
    data = np.load(data_path, allow_pickle = True)
    label = np.load(label_path, allow_pickle = True)
    data_split = np.split(data,task_num)
    label_split = np.split(label,task_num)

    init_time = time.time()
    for idx in range(task_num): 
        res = requests.post(f'{base_url}/project/data/upload',data = { # 업로드 url 요청
            'project_uid' : project_uid,
            'data'  : f'train_data_{idx}',
            'label'  : f'train_label_{idx}',
            'index'  : idx
        }, headers = {'AUTH' : get_auth_header()})

        url = res.json()['label_url'] # presigned url
        with TemporaryFile() as tf : 
            np.save(tf, label_split[idx])
            _ = tf.seek(0)
            requests.put(url = url,data = tf) # 라벨 업로드

        url = res.json()['data_url'] # presigned url
        with TemporaryFile() as tf : 
            np.save(tf, data_split[idx])
            _ = tf.seek(0)
            requests.put(url = url,data = tf) # 데이터 업로드
        print(f'{idx} uploaded')

    print('data uploading finished')
    print(time.time() - init_time)
    
def upload_model(model_path, project_uid): 
    res = requests.post(f'{base_url}/project/model/upload',data = { # 업로드 url 요청
        'project_uid' : project_uid,
        'model' : 'model.json'
    }, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)

    url = res.json()['model_url'] # presigned url

    with open(model_path, 'rb') as f : 
        requests.put(url = url,data = f) # 데이터 업로드
        
    print('model successfully uploaded')

def get_weight(project_id,params = None): 
    res = requests.get(f'{base_url}/project/{project_id}/project/weight', params = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)

    with TemporaryFile() as tf : 
        tf.write(res.content)
        _ = tf.seek(0)
        weight  = np.load(tf,allow_pickle = True)

    return weight

# 학습 시작 요청
def start_learning(project_id, params = None): 
    callback.stop_learning_tok = False

    res = requests.get(f'{base_url}/project/{project_id}/task/get', params = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    res_json = res.json()
    print(res_json)

    if(not(res_json['is_successful']))  : return 'FAIL'
    occupy_task(project_id,{'task_index' : res_json['task_index']})

    model_url = res_json['model_url']
    data_url = res_json['data_url']
    label_url = res_json['label_url']

    start_time = time.time()

    with TemporaryFile() as tf : 
        tf.write(requests.get(url = model_url).content)
        _ = tf.seek(0)
        model = keras.models.load_model(h5py.File(tf,mode = 'r'))

    with TemporaryFile() as tf : 
        tf.write(requests.get(url = data_url).content)
        _ = tf.seek(0)
        train_data = np.asarray(np.load(tf,allow_pickle = True)).astype(np.float32)

    with TemporaryFile() as tf : 
        tf.write(requests.get(url = label_url).content)
        _ = tf.seek(0)
        train_label = np.asarray(np.load(tf,allow_pickle = True)).astype(np.float32)

    init_weight = get_weight(project_id)

    model.set_weights(init_weight.tolist())
    task_index = int(res_json['task_index'])
    epoch = int(res_json['epoch'])
    batch_size = int(res_json['batch_size'])
    valid_rate = float(res_json['valid_rate'])

    print(train_data.shape)

    if(task_index  ==  -1)  : 
        validate(project_id)
        return 'STOP'
    
    try : 
        model.fit(train_data, train_label, batch_size = batch_size, epochs = epoch, validation_split = valid_rate, callbacks = [callback], verbose = 2)    
    except ValueError as e : 
        report_error(project_id = project_id,params = {'error_message' : e})
        return 'ERROR'
    except TypeError as e : 
        report_error(project_id = project_id,params = {'error_message' : e})
        return 'ERROR'

    if callback.stop_learning_tok : 
        return 'STOP'

    spent_time = time.time() - start_time

    with TemporaryFile() as tf : 
        np.save(tf, np.array(model.get_weights(),dtype = object) - np.array(init_weight,dtype = object))
        _ = tf.seek(0)
        update_success =  update_learning(project_id = project_id,
            params = {'task_index' : res_json['task_index'],'spent_time' : spent_time},
            gradient = {'gradient' : tf})

    if(not(update_success))  : return 'FAIL'

    return 'SUCCESS'

def report_error(project_id, params = None): 
    res = requests.post(f'{base_url}/project/{project_id}/report/',data = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    return res.json()['is_successful']

# 학습 Task 선점하기
def occupy_task(project_id, params = None): 
    res = requests.post(f'{base_url}/project/{project_id}/task/start/',data = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    return res.json()['is_successful']

# 학습 결과 전송하기
def update_learning(project_id, gradient, params = None): 
    res = requests.post(f'{base_url}/project/{project_id}/task/update/',files = gradient, data = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    return res.json()['is_successful']

def is_project_finished(project_id, params = None): 
    res = requests.get(f'{base_url}/project/{project_id}/finished', params = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)

    return res.status_code !=  270

# 결과 요청
def result_learning(project_id, params = None): 
    res = requests.get(f'{base_url}/project/{project_id}/result', params = params, headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)

    with TemporaryFile() as tf : 
        tf.write(res.content)
        _ = tf.seek(0)
        weight = np.load(tf,allow_pickle = True)
    return weight

# 중단 요청
def stop_learning(path, params, data = None): 
    res = requests.put(f'{base_url}/{path}', params = params, json = data, headers = get_auth_header())

    response_alert(res.status_code)
    return res.json()

# 진행 상태 요청
def status_req(path, params): 
    res = requests.get(f'{base_url}/{path}', params = params, headers = get_auth_header())

    response_alert(res.status_code)
    return res.json()


def validate(project_id): 
    model = get_model()

    weight = result_learning(project_id)
    model.set_weights(weight.tolist())

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose = 2)
    print('result is...')
    print(test_loss, test_acc)

def get_all_progress(): 
    res = requests.get(f'{base_url}/project/progress/', headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    return res.json()

def get_current_credit(): 
    res = requests.get(f'{base_url}/credit/remains/', headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    print(res.json())
    return res.json()

def get_credit_log(): 
    res = requests.get(f'{base_url}/credit/log/', headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    print(res)
    return res.json()

def get_owned_projects(): 
    res = requests.get(f'{base_url}/project/owned/', headers = {'AUTH' : get_auth_header()})
    response_alert(res.status_code)
    return res.json()

def verify_email(data = None): 
    res = requests.post(f'{base_url}/auth/send/email/', data = data)

    response_alert(res.status_code)
    return res.json()

def verify_code(data = None): 
    res = requests.post(f'{base_url}/auth/check/code/', data = data)

    response_alert(res.status_code)
    return res.json()

def verify_username(data = None): 
    res = requests.post(f'{base_url}/auth/check/username/', data = data)

    response_alert(res.status_code)
    return res.json()


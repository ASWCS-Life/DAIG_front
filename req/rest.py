import requests

from auth import get_auth_header

base_url = 'http://localhost:3000'

# rest api
def model_upload(path, data=None):
    res = requests.post(f'{base_url}/{path}', json=data, headers=get_auth_header())

    #if res.status_code not in [200, 201, 204]:
    #raise exc.ResponseException(res)
    print(data)
    return res.json()

# 학습 시작 요청
def start_learning(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

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
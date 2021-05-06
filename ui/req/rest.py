import requests

from .auth import get_auth_header

base_url = 'http://127.0.0.1:8000'

# post ()
def post(path, data=None):
    res = requests.post(f'{base_url}/{path}', data=data, headers=get_auth_header())
    print(base_url)
    if res.status_code not in [200, 201, 204]:
        raise SystemExit(requests.exceptions.HTTPError)
    return res.json()

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

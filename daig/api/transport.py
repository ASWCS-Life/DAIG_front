from auth import get_auth_header
import requests

base_url = ''


def get(path, params=None):
    requests.get(f'{base_url}/{path}', params=params, header=get_auth_header())

    if response.status_code not in [200, 201, 204]:
        raise exc.ResponseException(response)
    return response.json()


def post(path, data=None):
    requests.post(f'{base_url}/{path}', json=data, header=get_auth_header())

    if response.status_code not in [200, 201, 204]:
        raise exc.ResponseException(response)
    return response.json()


def put(path, data=None):
    requests.put(f'{base_url}/{path}', json=data, header=get_auth_header())

    if response.status_code not in [200, 201, 204]:
        raise exc.ResponseException(response)
    return response.json()

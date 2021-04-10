from .api.transport import *
from .api.auth import header


def login(username, password):
    data = {
        "username": username,
        "password": password
    }
    res = post('login', data)

    header = res.get('auth')
    print(res["message"])
    return

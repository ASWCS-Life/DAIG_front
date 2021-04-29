import requests

import numpy as np

from tensorflow.keras import layers, models, datasets

from auth import get_auth_header

# 데이터 준비
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

train_images, test_images = train_images / 255.0, test_images / 255.0

# 데이터 분할

def data_division(train_images, train_lables, num):
    model_list = []
    train_img_list = []
    train_lbl_list = []
    for i in range(num):
        img_div_pos = (len(train_images)//num)*(i)
        img_div_end = (len(train_images)//num)*(i+1)
        lbl_div_pos = (len(train_lables) // num) * (i)
        lbl_div_end = (len(train_lables) // num) * (i + 1)

        train_img_list.append(train_images[img_div_pos:img_div_end])
        train_lbl_list.append(train_labels[lbl_div_pos:lbl_div_end])

        model_list.append(models.Sequential())
        model_list[i].add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        model_list[i].add(layers.MaxPooling2D((2, 2)))
        model_list[i].add(layers.Conv2D(64, (3, 3), activation='relu'))
        model_list[i].add(layers.MaxPooling2D((2, 2)))
        model_list[i].add(layers.Conv2D(64, (3, 3), activation='relu'))
        model_list[i].add(layers.Flatten())
        model_list[i].add(layers.Dense(64, activation='relu'))
        model_list[i].add(layers.Dense(10, activation='softmax'))

    return train_img_list, train_lbl_list, model_list

TIL, TLL, ML = data_division(train_images, train_labels, 5)

# np.array 로 변환
Til_np = np.array(TIL)
Tll_np = np.array(TLL)
Tst_img_np = np.array(test_images)
Tst_lbl_np = np.array(test_labels)


base_url = 'http://localhost:3000'

# 예시로 한명만
individual_data = {
    "data":ML[1].to_json()
}


# 모델 데이터 업로드
def upload(path, data=None):
    res = requests.post(f'{base_url}/{path}', json=data, headers=get_auth_header())

    #if res.status_code not in [200, 201, 204]:
    #raise exc.ResponseException(res)
    print(data)
    return res.json()

# 학습 시작 요청
def start(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

    #if res.status_code not in [200, 201, 204]:
    #raise exc.ResponseException(res)
    return res.json()


def result(path, params=None):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.json()


def stop(path, params, data=None):
    res = requests.put(f'{base_url}/{path}', params=params, json=data, headers=get_auth_header())

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.json()


def status(path, params):
    res = requests.get(f'{base_url}/{path}', params=params, headers=get_auth_header())

    # if res.status_code not in [200, 201, 204]:
    # raise exc.ResponseException(res)
    return res.json()

upload('users',individual_data)
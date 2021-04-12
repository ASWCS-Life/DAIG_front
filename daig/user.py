from .api.transport import *
from .api.auth import header

from tensorflow.keras import datasets, layers, models

temporary_training_data # gonna be erased later.

def login(username, password):
    data = {
        "username": username,
        "password": password
    }
    res = post('login', data)

    header = res.get('auth')
    print(res["message"])
    return


def distributed_learn():
    req = get('learn')

    model_json = req['model']
    model = models.model_from_json(model_json)

    # 아래 model은 더미 모델입니다. 실제로는 req의 데이터를 이용할 예정
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
    
    prev_weight = model.get_weights()
    
    train_data = load_train_data()
    model.fit(train_data.x, train_data.y)

    trained_weight = model.get_weights()

    gradient = trained_weight - prev_weight

    data = {'gradient' : gradient}
    res = post('learnResult', data)


def load_train_data():
    res = get('dataload')
    dara_url = res['url']

    # 여기에 S3에서 학습 데이터를 가져오는 코드를 짜주세요
    # 위의 res는 서버에서 받아오는 URL을 의미하고, 다음 res는 S3에서 받아온 실제 학습 데이터를 의미
    #

    return res['data']   

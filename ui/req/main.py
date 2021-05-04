import numpy as np

import rest

from tensorflow.keras import layers, models, datasets

# 데이터 준비
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

train_images, test_images = train_images / 255.0, test_images / 255.0

# 모델 생성
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))


# np파일명 설정
def set_file_name(info, num):
    file_name = info
    if (len(str(num)) == 1):
        file_name += ('00' + str(num))
    elif (len(str(num)) == 2):
        file_name += ('0' + str(num))
    else:
        file_name += str(num)
    return file_name + '.npy'

# 데이터 분할
def data_division(train_images, train_lables, num=100):
    for i in range(num):
        img_div_pos = (len(train_images) // num) * i
        img_div_end = (len(train_images) // num) * (i + 1)
        lbl_div_pos = (len(train_lables) // num) * i
        lbl_div_end = (len(train_lables) // num) * (i + 1)

        img_file_name = set_file_name('img', i + 1)
        lbl_file_name = set_file_name('lbl', i + 1)
        np.save('./np_data/train_img/train_' + img_file_name, train_images[img_div_pos:img_div_end])
        np.save('./np_data/train_lbl/train_' + lbl_file_name, train_lables[lbl_div_pos:lbl_div_end])
    return

# 분할 예시
#data_division(train_images, train_labels, 100)

# 모델 데이터 전송 예시
individual_data = {
    "data":model.to_json()
}
rest.model_upload('users', individual_data)

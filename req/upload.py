#!/usr/bin/env python
# coding: utf-8

# In[1]:


#req to server
import requests

import tensorflow

from tensorflow.keras import layers, models, datasets

from auth import get_auth_header


# In[2]:


(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

train_images, test_images = train_images / 255.0, test_images / 255.0


# In[3]:


model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.summary()


# In[16]:


base_url = 'http://localhost:3000'

project_id = '01'

status = 'stop learning'

data_info = {
      "model" : model.to_json(),
      "data" : [train_images, test_images]
}

# "data" : 스트링 타입 ..?


# In[12]:


# 모델 데이터 업로드

def upload(path, data = None):
    res = requests.post(f'{base_url}/{path}', json = data, headers = get_auth_header())
    
    #if res.status_code not in [200, 201, 204]:
       # raise exc.ResponseException(res)
    return res.json()


# In[6]:


# 학습 시작 요청


def start(path, params = None):
    res = requests.get(f'{base_url}/{path}', params = params, headers = get_auth_header())
    
    #if res.status_code not in [200, 201, 204]:
        #raise exc.ResponseException(res)
    return res.json()


# In[7]:


#학습 결과 요청

def result(path, params = None):
    res = requests.get(f'{base_url}/{path}', params = params, headers = get_auth_header())
    
    #if res.status_code not in [200, 201, 204]:
        #raise exc.ResponseException(res)
    return res.json()


# In[8]:


#학습 중단 요청

def stop(path, params ,data = None):
    res = requests.put(f'{base_url}/{path}', params = params, json = data, headers = get_auth_header())
    
    #if res.status_code not in [200, 201, 204]:
        #raise exc.ResponseException(res)
    return res.json()


# In[9]:


# 학습 현황 확인

def status():
    res = requests.get(f'{base_url}/{path}', params = params, headers = get_auth_header())
    
    #if res.status_code not in [200, 201, 204]:
        #raise exc.ResponseException(res)
    return res.json()


# In[17]:


upload('users',data_info)


# In[ ]:





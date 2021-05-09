# state value 들의 get / set 함수

# 프로젝트 생성시 p_id를 받음
p_id = ''

def get_p_id():
    return p_id

def set_p_id(id):
    p_id = id

# 프로젝트 종료시 total spend time을 받음

total_time = '0'

def get_total_time():
    return total_time

def set_total_time(t):
    total_time = t

# UI에서 파일을 올리면 파일 절대 경로를 받게됨
train_data_path_list = ''

model_path = ''

def get_train_data_path():
    return train_data_path_list

def set_train_data_path(path_list):
    train_data_path_list = path_list

def get_model_path():
    return model_path

def set_model_path(mdl_path):
    model_path = mdl_path
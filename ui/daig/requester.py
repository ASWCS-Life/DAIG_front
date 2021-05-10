# state value 들의 get / set 함수

import os

# # 프로젝트 생성시 project_uid를 받음
# project_uid = ''

# def get_project_uid():
#     return project_uid

# def set_project_uid(id):
#     project_uid = id

# # 프로젝트 종료시 total spend time을 받음

# total_time = '0'

# def get_total_time():
#     return total_time

# def set_total_time(t):
#     total_time = t

# # UI에서 파일을 올리면 파일 절대 경로를 받게됨
# train_dir_path = ''

# model_path = ''

# def get_train_dir_path():
#     return train_dir_path

# def set_train_dir_path(dir_path):
#     train_dir_path = dir_path

# def get_model_path():
#     return model_path

# def set_model_path(mdl_path):
#     model_path = mdl_path


# img, lbl 파일 path 2차원 배열 matrix

class Project():
    def __init__(self):
        self.uid=''
        self.spent_time = ''
        self.train_dir_path = ''
        self.model_path = ''



project=Project()

    
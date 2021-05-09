# state value 들의 get / set 함수

import os

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
train_dir_path = ''

model_path = ''

def get_train_dir_path():
    return train_dir_path

def set_train_dir_path(dir_path):
    train_dir_path = dir_path

def get_model_path():
    return model_path

def set_model_path(mdl_path):
    model_path = mdl_path


# img, lbl 파일 path 2차원 배열 matrix

def data_division(task_num=100):
    # train_image, train_lable, validation_image, validation_lable
    train_img_folder_name = 'train_img'
    train_lbl_folder_name = 'train_lbl'
    #valid_img_folder_name = ''
    #valid_lbl_folder_name = ''
    train_img_path = get_train_dir_path() + '/' + train_img_folder_name
    train_lbl_path = get_train_dir_path() + '/' + train_lbl_folder_name
    #valid_img_path = get_train_dir_path() + '/' + valid_img_folder_name
    #valid_lbl_path = get_train_dir_path() + '/' + valid_lbl_folder_name

    train_img_matrix = division_by_task(train_img_path, task_num)
    train_lbl_matrix = division_by_task(train_lbl_path, task_num)
    #valid_img_matrix = division_by_task(valid_img_path, task_num)
    #valid_lbl_matrix = division_by_task(valid_lbl_list, task_num)
    
    #return train_img_matrix, train_lbl_matrix, valid_img_matrix, valid_lbl_matrix
    return train_img_matrix, train_lbl_matrix


# [[],[]] 2차원배열. task 0번째, 1번째 마다 총 파일의 개수를 task 수로 나눈만큼의 파일의 path들이 들어가 있도록.
def division_by_task(data_path, task_num):
    file_list = os.listdir(data_path)

    file_path_list = [[] for i in range(task_num)]
    for i in range(task_num):
        div_pos = (len(file_list) // task_num) * i
        div_end = (len(file_list) // task_num) * (i + 1)
        for j in range(div_pos, div_end+1):
            file_path_list[i].append(data_path + '/' + file_list[j])
    return file_path_list

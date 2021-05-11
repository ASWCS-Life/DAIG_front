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

# npy 파일 path 찾기
def find_npy_path(dir_path):
    # train_image, train_lable, validation_image, validation_lable
    train_img_dir_nm = 'train_img'
    train_lbl_dir_nm = 'train_lbl'
    #valid_img_dir_nm = ''
    #valid_lbl_dir_nm = ''
    train_img_dir_path = dir_path + '/' + train_img_dir_nm
    print(train_img_dir_path)
    train_lbl_dir_path = dir_path + '/' + train_lbl_dir_nm
    print(train_lbl_dir_path)
    #valid_img_dir_path = dir_path + '/' + valid_img_dir_nm
    #valid_lbl_dir_path = dir_path + '/' + valid_lbl_dir_nm

    train_img_path = npy_file_path(train_img_dir_path)
    print(train_img_path)
    train_lbl_path = npy_file_path(train_lbl_dir_path)
    print(train_lbl_path)
    #valid_img_path = npy_file_path(valid_img_dir_path)
    #valid_lbl_path = npy_file_path(valid_lbl_dir_list)

    #return train_img_path, train_lbl_path, valid_img_path, valid_lbl_path
    return train_img_path, train_lbl_path


# 예를들어 10000개의 이미지라면 10000개의 이미지가 concatenated 된 npy파일 하나라고 가정
def npy_file_path(data_path):
    file = os.listdir(data_path)
    print(file)

    file_path = data_path + '/' + file[0]
    return file_path

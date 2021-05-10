import sys
from daig.api.rest import *
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog

class DataUploadWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):

  # 파일 이름 출력
    self.model = QLabel('모델: ')
    self.data = QLabel('데이터: ')
    self.p_task_div = QLabel('Task 분할 개수')
    self.p_step_task = QLabel('Step별 task 개수')
    self.m_file_name = QLabel('')
    self.d_file_name = QLabel('')

  # 파일 올리는 버튼
    self.model_btn = QPushButton('올리기')
    self.model_btn.clicked.connect(self.model_btn_clicked)
    self.data_btn = QPushButton('올리기')
    self.data_btn.clicked.connect(self.file_btn_clicked)

  # task 분할 개수 출력
    self.cho_task = QComboBox()
    task_num = 10
    while task_num <= 100:
      self.cho_task.addItem(str(task_num))
      task_num += 1
    self.cho_task.activated.connect(self.print_choice_task)

  # step별 task 개수
    self.cho_step = QComboBox()
    step_num = 1
    while step_num <= 10:
      self.cho_step.addItem(str(step_num))
      step_num += 1
    self.cho_step.activated.connect(self.print_choice_step)

  # 학습 시작 버튼
    self.train_start = QPushButton('프로젝트 생성')
    self.train_start.clicked.connect(self.train_start_clicked)

    # 레이아웃 설정 및 출력
    layout = QGridLayout()
    layout.addWidget(self.model, 0, 0)
    layout.addWidget(self.m_file_name, 0, 1)
    layout.addWidget(self.model_btn, 0, 2)
    layout.addWidget(self.data, 1, 0)
    layout.addWidget(self.d_file_name, 1, 1)
    layout.addWidget(self.data_btn, 1, 2)

    layout.addWidget(self.p_task_div, 3, 0)
    layout.addWidget(self.cho_task, 3, 2)
    layout.addWidget(self.p_step_task, 4, 0)
    layout.addWidget(self.cho_step, 4, 2)
    layout.addWidget(self.train_start, 5, 2)

    self.setLayout(layout)

    # task 분할 개수 출력

  def print_choice_task(self, text):
    self.cho_task.setEditText(str(text))
    self.cho_task.adjustSize()

    # step별 task 분할 개수 출력

  def print_choice_step(self, text):
    self.cho_step.setEditText(str(text))
    self.cho_step.adjustSize()

  # 모델 파일 받아오기 / 하나의 py파일만 선택 가능
  def model_btn_clicked(self):
    self.m_file = QFileDialog.getOpenFileName(self, filter="*.py")
    self.m_file_name.setText(self.m_file[0])
    print(self.m_file)
    print(self.m_file[0])
    set_model_path(self.m_file[0])

  # 데이터 파일 받아오기 / 복수의 npy 파일 선택 가능 - 선택된 파일들을 리스트로 리턴
  def file_btn_clicked(self):
    self.d_file = QFileDialog.getExistingDirectory(self)
    self.d_file_name.setText(str(self.d_file))
    print(self.d_file)
    set_train_dir_path(self.d_file)

  # '프로젝트 생성' 버튼을 눌렀을 때 설정한 task, step 수 및 모델, 훈련 데이터를 받아와서...
  # 프로젝트 생성 버튼에 '프로젝트 생성' 요청
  def train_start_clicked(self):

    task_num = int(self.cho_task) # 분할할 task 수
    step_num = int(self.cho_step) # step내 task 수
    train_img_mtrx, train_lbl_mtrx = self.data_division(task_num) # check dummyData.js
    model_path = 'test_path' # get_model_path() #여기서 model은 요청자가 올린 model py파일의 path임
    train_data_path = 'test_path' # get_train_data_path() #요청자가 올린 npy파일 path의 list가 들어감

    # dummy model for test
    model = get_model()

    task_num = int(self.cho_task.currentText()) # 분할할 task 수
    step_num = int(self.cho_step.currentText()) # step내 task 수

    res = create_project(model.get_weights(), data = {
        'rrs':train_data_path,
        'model_url':model_path,
        'total_task':task_num,
        'step_size':step_num
      })

    # set_p_id(res["project_id"])

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

    train_img_matrix = self.division_by_task(train_img_path, task_num)
    train_lbl_matrix = self.division_by_task(train_lbl_path, task_num)
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



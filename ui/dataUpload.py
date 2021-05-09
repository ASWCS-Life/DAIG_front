import sys
from req.rest import *
from component.dummyData import *
from PyQt5.QtWidgets import *

class data_upload(QWidget):
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
    self.d_file = QFileDialog.getOpenFileNames(self, filter="*.npy")
    self.d_file_name.setText(str(self.d_file[0]))
    print(self.d_file)
    print(self.d_file[0])
    set_train_data_path(self.d_file[0])

  # '프로젝트 생성' 버튼을 눌렀을 때 설정한 task, step 수 및 모델, 훈련 데이터를 받아와서...
  # 프로젝트 생성 버튼에 '프로젝트 생성' 요청
  def train_start_clicked(self):
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

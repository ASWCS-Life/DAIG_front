import os
from daig.api.rest import *
from PyQt5.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog
from daig.requester import project
from component.constants import setLabelStyle, setButtonStyle, setLoginButtonStyle

class DataUploadWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):

    # 파일 이름 출력
    self.model = QLabel('model')
    self.train_img = QLabel('train image')
    self.train_lbl = QLabel('train label')
    #self.valid_img = QLabel('valid image')
    #self.valid_lbl = QLabel('valid label')
    self.p_contributer = QLabel('max contributer : ')
    self.p_task_div = QLabel('Task 분할 개수')
    self.p_step_task = QLabel('Step별 task 개수')
    self.model_path = QLabel('')
    self.model_path.setMinimumSize(250, 20)
    self.train_img_path = QLabel('')
    self.train_lbl_path = QLabel('')
    #self.valid_img_path = QLabel('')
    #self.valid_lbl_path = QLabel('')

    setLabelStyle(self.model)
    setLabelStyle(self.train_img)
    setLabelStyle(self.train_lbl)
    setLabelStyle(self.p_task_div)
    setLabelStyle(self.p_step_task)

  # 파일 올리는 버튼
    self.model_btn = QPushButton('올리기')
    self.model_btn.clicked.connect(self.model_btn_clicked)
    self.train_img_btn = QPushButton('올리기')
    self.train_img_btn.clicked.connect(self.train_img_btn_clicked)
    self.train_lbl_btn = QPushButton('올리기')
    self.train_lbl_btn.clicked.connect(self.train_lbl_btn_clicked)
    #self.valid_img_btn = QPushButton('올리기')
    #self.valid_img_btn.clicked.connect(self.train_img_btn_clicked)
    #self.valid_img_btn = QPushButton('올리기')
    #self.valid_img_btn.clicked.connect(self.train_lbl_btn_cliked)

 # task 분할 개수 출력
    self.cho_task = QLineEdit(self)

  # step별 task 개수
    self.cho_step = QLineEdit(self)

  # 학습 시작 버튼
    self.train_start = QPushButton('프로젝트 생성')
    self.train_start.clicked.connect(self.train_start_clicked)
    setButtonStyle(self.train_start)

    # 레이아웃 설정 및 출력
    layout = QGridLayout()
    layout.addWidget(self.model, 0, 0)
    layout.addWidget(self.model_path, 0, 1)
    layout.addWidget(self.model_btn, 0, 2)
    layout.addWidget(self.train_img, 1, 0)
    layout.addWidget(self.train_img_path, 1, 1)
    layout.addWidget(self.train_img_btn, 1, 2)
    layout.addWidget(self.train_lbl, 2, 0)
    layout.addWidget(self.train_lbl_path, 2, 1)
    layout.addWidget(self.train_lbl_btn, 2, 2)
    layout.addWidget(self.p_task_div, 3, 0)
    layout.addWidget(self.cho_task, 3, 2)
    layout.addWidget(self.p_step_task, 4, 0)
    layout.addWidget(self.cho_step, 4, 2)
    layout.addWidget(self.train_start, 5, 2)

    self.setLayout(layout)

  # task 분할 개수 출력
  def onChanged(self, text):
    self.cho_task.setText(text)
    self.id.adjustSize()
    self.cho_step.setText(text)
    self.pwd.adjustSize()

  # 모델 파일 받아오기 / 하나의 디렉토리로 받아옵니다. Tensorflow Model Format 참조
  def model_btn_clicked(self):
    self.m_file = QFileDialog.getOpenFileName(self, './', filter="*.h5")
    self.model_path.setText(self.m_file[0])

  # train img 파일 받아오기
  def train_img_btn_clicked(self):
    self.train_img_file = QFileDialog.getOpenFileName(self, './', filter="*.npy")
    self.train_img_path.setText(self.train_img_file[0])

    #self.train_img_path.text() : 받아온 학습 이미지 경로
  # train lbl 파일 받아오기
  def train_lbl_btn_clicked(self):
    self.train_lbl_file = QFileDialog.getOpenFileName(self, './', filter="*.py")
    self.train_lbl_path.setText(self.train_lbl_file[0])

    #self.train_lbl_path.text() : 받아온 학습 레이블 경로

  # '프로젝트 생성' 버튼을 눌렀을 때 설정한 task, step 수 및 모델, 훈련 데이터를 받아와서...
  # 프로젝트 생성 버튼에 '프로젝트 생성' 요청
  def train_start_clicked(self):

    task_num = int(self.cho_task.text()) # 분할할 task 수
    step_num = int(self.cho_step.text()) # step내 task 수
    # train_img_mtrx, train_lbl_mtrx = data_division(task_num) # check dummyData.js
    model_path = 'test_path' # get_model_path() #여기서 model은 요청자가 올린 model py파일의 path임
    train_data_path = 'test_path' # get_train_data_path() #요청자가 올린 npy파일 path의 list가 들어감

    # dummy model for test
    model = get_model()

    res = create_project(model.get_weights(), data = {
        'rrs':train_data_path,
        'model_url':model_path,
        'total_task':task_num,
        'step_size':step_num
      })

    # set_p_id(res["project_id"])
    project.uid=res["project_uid"]

    # dummy값이 아닌 ui에서 받아온 model과 npy파일들의 path
    # model_path = self.file_path.text()
    upload_model(self.model_path.text(),project.uid)
    upload_data(self.train_img_path.text(),self.train_lbl_path.text(),project.uid,task_num)
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from daig.dummyData import get_p_id, get_total_time

class TrainResultWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):
    # 창 띄우기

  # 학습 설정 출력
    self.p_set_train = QLabel('학습 결과')
    self.p_set_train.setAlignment(Qt.AlignCenter)

  # pID 출력
    self.p_pID_name = QLabel('pID: ')
    self.p_pID_name.setAlignment(Qt.AlignCenter)
    self.pID = QLabel(get_p_id(), self)
    self.pID.setAlignment(Qt.AlignCenter)

  # 소요시간
    self.p_spent_time = QLabel('소요 시간: ')
    self.p_spent_time.setAlignment(Qt.AlignCenter)
    self.spent_time = QLabel(get_total_time(), self)
    self.spent_time.setAlignment(Qt.AlignCenter)

  # loss / not yet
    self.p_loss = QLabel('Loss: ')
    self.p_loss.setAlignment(Qt.AlignCenter)
    self.loss = QLabel('', self)
    self.loss.setAlignment(Qt.AlignCenter)

  # accuracy / not yet
    self.p_accuracy = QLabel('Accuracy: ')
    self.p_accuracy.setAlignment(Qt.AlignCenter)
    self.accuracy = QLabel('', self)
    self.accuracy.setAlignment(Qt.AlignCenter)

  # 총지출
    self.p_all_credit = QLabel('총 지출: ')
    self.p_all_credit.setAlignment(Qt.AlignCenter)
    self.all_credit = QLabel('', self)
    self.all_credit.setAlignment(Qt.AlignCenter)

  # 모델 받기 버튼
    self.get_model = QPushButton('모델 받기', self)
    #self.start_task_btn.clicked.connect(self.get_model_fun) # 모델 받기 버튼(밑에 함수 있음)

  # 돌아가기 버튼
    self.go_back = QPushButton('돌아가기', self)
    # self.start_task_btn.clicked.connect(self.go_back_fun) # 돌아가기 버튼(밑에 함수 있음)

  # 레이아웃 설정 및 출력
    layout = QGridLayout()
    layout.addWidget(self.p_set_train, 0, 0, 1, 0)
    layout.addWidget(self.p_pID_name, 1, 0)
    layout.addWidget(self.pID, 0, 1)
    layout.addWidget(self.p_spent_time, 2, 0)
    layout.addWidget(self.spent_time, 2, 1)
    layout.addWidget(self.p_loss, 3, 0)
    layout.addWidget(self.loss, 3, 1)
    layout.addWidget(self.p_accuracy, 4, 0)
    layout.addWidget(self.accuracy, 4, 1)
    layout.addWidget(self.p_all_credit, 2, 2)
    layout.addWidget(self.all_credit, 2, 3)
    layout.addWidget(self.get_model, 5, 2)
    layout.addWidget(self.go_back, 5, 3)

    self.setLayout(layout)

  # 모델 받기 (우선 함수 설정)
  def get_model_fun(self):
    self.get_model.setText('model')

  # 돌아가기 (우선 함수 설정)
  def go_back_fun(self):
    self.go_back.setText('goback')

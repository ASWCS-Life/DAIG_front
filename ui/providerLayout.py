from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from req.main import *
from req.rest import *


class ProviderWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):
    self.train_start = QPushButton('학습 시작')
    self.train_stop = QPushButton('학습 중단')
    self.train_stop.setEnabled(False)
    self.train_start.clicked.connect(self.onTrainButtonClicked)

  # 사용자 페이지
    grid = QGridLayout()
    grid.addWidget(self.show_user(), 0, 0)
    grid.addWidget(self.train_start, 1, 0)
    grid.addWidget(self.train_stop, 1, 1)

    self.setLayout(grid)

  def show_user(self):
    user_box = QGroupBox('사용자 프로필')
    user_id = QLabel('ID')
    user_credit = QLabel('Credit')

    user_layout = QHBoxLayout()
    user_layout.addWidget(user_id)
    user_layout.addWidget(user_credit)
    user_box.setLayout(user_layout)

    return user_box

    # 학습 시작 버튼을 눌렀을 경우
  def onTrainStartClicked(self):
      self.train_start.setEnabled(False)
      self.train_stop.setEnabled(True)

    # 학습 중단 버튼을 눌렀을 경우
  def onTrainStopClicked(self):
      self.train_start.setEnabled(True)
      self.train_stop.setEnabled(False)

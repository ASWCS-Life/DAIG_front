from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread
import time

from daig.api.main import *
from daig.api.rest import get_avaiable_project, start_learning, start_learning_internal, stop_learning_internal, is_project_finished

from daig.api.auth import get_auth_header, set_auth_header

class Worker(QThread):
  stop_learning = False

  def __init__(self, parent=None):
    super(Worker, self).__init__(parent)
    set_auth_header({'key':get_auth_header()})

  def run(self):
    self.stop_learning = False
    start_learning_internal()
    project_id = get_avaiable_project()
    if(project_id == -1): return
    result = start_learning(project_id)
    if((result == 'STOP') or (result == 'FAIL')):
      return
    time.sleep(2)
    if(not(self.stop_learning)):
      self.run()

  def stop(self):
    self.stop_learning = True
    stop_learning_internal()


class ProviderWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()
    self.project_id = -1
    self.worker = Worker()

  # code
  def init_ui(self):
    self.train_start = QPushButton('학습 시작')
    self.train_stop = QPushButton('학습 중단')
    self.train_stop.setEnabled(False)
    self.train_start.clicked.connect(self.onTrainStartClicked)
    self.train_stop.clicked.connect(self.onTrainStopClicked)

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
      self.repeat_learning()

    # 학습 중단 버튼을 눌렀을 경우
  def onTrainStopClicked(self):
      self.train_start.setEnabled(True)
      self.train_stop.setEnabled(False)
      self.worker.stop()

  def repeat_learning(self):
    self.project_id = get_avaiable_project()

    if(self.project_id == -1):
      self.worker.stop()
      return

    self.worker.setTerminationEnabled(True)
    self.worker.start()
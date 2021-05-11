from PyQt5 import QtGui
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QThread, QTimer, Qt
from daig.api.rest import get_avaiable_project, start_learning
import time
from daig.api.auth import get_auth_header

class Worker(QThread):
  def __init__(self, parent=None):
    super(Worker, self).__init__(parent)

  def run(self):
    project_id = get_avaiable_project()
    start_learning(project_id, get_auth_header())
    start_learning(project_id, get_auth_header())
  def stop(self):
    pass
    #self.quit()
    #self.wait()


# create
class ProgressWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()
    self.project_id = -1
    self.worker = Worker()

  # code
  def init_ui(self):
  # 레이아웃
    layout = QGridLayout()
    self.setLayout(layout)

  # 학습 진행중 / 중단 알림
    self.indicator = QLabel('분산학습 준비 완료')
    self.indicator.setAlignment(Qt.AlignCenter)
    layout.addWidget(self.indicator, 0, 1)

  # 실시간 사용된 데이터와 크레딧
    self.used_data = QLabel('')
    self.used_credit = QLabel('')
    self.used_data.setAlignment(Qt.AlignCenter)
    self.used_credit.setAlignment(Qt.AlignCenter)
    layout.addWidget(self.used_data, 1, 0)
    layout.addWidget(self.used_credit, 1, 1)


# 학습 진행중 - loading animation
    self.label = QLabel(self)
    self.label.setAlignment(Qt.AlignCenter)
    self.movie = QtGui.QMovie("./local_data/loading.gif", QByteArray(), self)
    self.movie.setCacheMode(QMovie.CacheAll)
    self.movie.setSpeed(100)
    self.label.setMovie(self.movie)
    layout.addWidget(self.label, 2, 1)

  # 학습 시작, 중단 및 결과 확인 버튼
    self.start_btn = QPushButton('학습 시작', self)  # bar button
    self.stop_btn = QPushButton('학습 중단', self)
    self.result_btn = QPushButton('결과 확인', self)
    self.result_btn.setEnabled(False)

  # 학습 현황 확인 / 2초마다 학습 현황 요청
    self.prgs_info = QLabel("현황 확인 중..")
    self.start_time = time.time() # 총 소요시간은 재기위한 타이머 / 학습 중단이 들어가면 스톱워치 기능 구현해야함
    self.timer = QTimer(self)  # 진행상태를 요청하기 위한 타이머
    self.timer.setInterval(2000)
    self.timer.timeout.connect(self.onProgressHandler)
    self.timer.start()
    layout.addWidget(self.prgs_info, 2, 2)
    self.prgs_info.setAlignment(Qt.AlignCenter)

  # 버튼 설정
    layout.addWidget(self.result_btn, 3, 1)
    layout.addWidget(self.start_btn, 3, 2)
    layout.addWidget(self.stop_btn, 3, 3)

  # 버튼 클릭시 메세지 출력
    self.start_btn.clicked.connect(self.onStartHandler)
    self.stop_btn.clicked.connect(self.onStopHandler)

  # 학습 요청
  def onStartHandler(self):
    self.movie.start()
    self.indicator.setText('분산학습 진행중..')
    self.repeat_learning()

    #res = project_start() / req.rest
    #self.loading.start()

  # 학습 현황 확인 / 2초 마다 트리거 됨
  def onProgressHandler(self):
    #res = project_progress() / req.rest
    #if (res["float"] == 1) onEndHandler()
    #else: print(res["message"])
    return

  #학습 중단
  def onStopHandler(self):
    self.movie.stop()
    self.prgs_info.setText('분산학습이 중단되었습니다.')
    self.worker.stop()

    #res = project_status() / req.rest
    #self.loading.stop()

  # 학습 완료 / 학습진행상태를 확인했을때 학습이 끝났으면 '결과확인'버튼을 활성화 함
  # def onEndHandler(self):
    #self.result_btn.setEnabled(True)

    #set_total_time(str(time.time() - self.start_time))

  def repeat_learning(self):
    if(self.project_id != -1):
      if is_project_finished(self.project_id):
        validate(self.project_id)

    self.project_id = get_avaiable_project()

    if(self.project_id == -1):
      self.prgs_info.setText('현재 참여 가능한 프로젝트가 없습니다.')
      self.worker.stop()
      return

    self.prgs_info.setText('분산 학습이 진행중입니다...')

    self.worker.setTerminationEnabled(True)
    self.worker.start()

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from req.main import *
from req.rest import *

class userFrame(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):

  # 사용자 페이지
    grid = QGridLayout()
    grid.addWidget(self.show_file(), 0, 0, 0, 1)
    grid.addWidget(self.show_user(), 0, 1)
    grid.addWidget(self.show_studying(), 1, 1)

    self.setLayout(grid)

  def show_file(self):
    file_box = QGroupBox('파일 요청 목록(전에 실행/ 실행중)')
    lable1 = QLabel('분산학습1')
    lable2 = QLabel('분산학습2')

    file_layout = QVBoxLayout()
    file_layout.addWidget(lable1)
    file_layout.addWidget(lable2)
    file_box.setLayout(file_layout)

    return file_box

  def show_user(self):
    user_box = QGroupBox('사용자 프로필')
    user_id = QLabel('ID')
    user_credit = QLabel('Credit')

    user_layout = QHBoxLayout()
    user_layout.addWidget(user_id)
    user_layout.addWidget(user_credit)
    user_box.setLayout(user_layout)

    return user_box

  def show_studying(self):
    project_box = QGroupBox('분산학습 시작')
    self.project_create = QPushButton('프로젝트 생성')
    self.project_upload = QPushButton('데이터 업로드')
    self.project_start = QPushButton('학습 요청')
    self.project_result = QPushButton('결과 확인')

    project_layout = QHBoxLayout()
    project_layout.addWidget(self.project_create)
    project_layout.addWidget(self.project_upload)
    project_layout.addWidget(self.project_start)
    project_layout.addWidget(self.project_result)
    project_box.setLayout(project_layout)

    return project_box

  # 프로젝트 생성
  def createProject(self):
    res = get("project/create")
    if(res["is_successful" == True]):
      QMessageBox.about(self, 'DAIG', res["message"], res["project_uid"])
      p_id = res["project_uid"]
      print(res)
      return p_id
    else:
      QMessageBox.about(self, 'DAIG', res["message"])
      return False

  # 생성한 프로젝트의 데이터 업로드
  def uploadData(self, p_id):
    data = dataPreparation()
    res = post(f"project/{p_id}/upload", data)
    if(res["is_successful" == True]):
      QMessageBox.about(self,'DAIG', res["message"])
      return True
    else:
      QMessageBox.about(self, 'DAIG', res["message"])
      return False

  # 프로젝트 시작요청
  def startProject(self, p_id):
    res = get(f"project/{p_id}/start")
    if (res["is_successful" == True]):
      QMessageBox.about(self, 'DAIG', res["message"])
      return True
    else:
      QMessageBox.about(self, 'DAIG', res["message"])
      return False

  # 프로젝트 결과 요청
  def resultProject(self, p_id):
    res = get(f"project/{p_id}/result")
    if (res["is_successful" == True]):
      QMessageBox.about(self, 'DAIG', res["message"])
      print(res)
      return res["model"]
    else:
      QMessageBox.about(self, 'DAIG', res["message"])
      return False

# MainWindow UI
class userWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.user_frame = userFrame()
    self.setCentralWidget(self.user_frame)

    # 툴바 아이콘 지정 및 헹동 지정
    go_home = QAction(QIcon('./local_data/home.png'), 'Home', self)
    go_home.setStatusTip('Home')
    go_home.triggered.connect(qApp.quit)  # 아이콘 클릭시 (우선 창 닫기로 설정)

    self.toolbar = self.addToolBar('Home')
    self.toolbar.addAction(go_home)

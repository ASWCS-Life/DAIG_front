import sys
from PyQt5.QtWidgets import QSizePolicy,QWidget, QLabel,QMainWindow, QApplication, QStackedWidget, QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from component.center import on_layout_convert_center

from login import LoginWidget
from signUp import SignUpWidget
from mode import ModeChoiceWidget
from userLayout import UserFrameWidget
from providerLayout import ProviderWidget
from trainResult import TrainResultWidget
from progress import ProgressWidget
from dataUpload import DataUploadWidget


# 학습 결과 화면 - widget_index_num : 7
class TrainResult(TrainResultWidget):
    def __init__(self):
        super().__init__()
        #self.get_model.clicked.connet(self.openModelInfoHandler)

    def openModelInfoHandler(self):
        return


# 진행 상황 - widget_index_num : 6
class Progress(ProgressWidget):
    def __init__(self):
        super().__init__()
        self.result_btn.clicked.connect(self.openProgressClassHandler)

    def openProgressClassHandler(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        on_layout_convert_center(main_window, widget, 500, 500)


# 데이터 업로드 화면 - widget_index_num : 5
class DataUploadLayout(DataUploadWidget):
    def __init__(self):
        super().__init__()
        # self.train_start.clicked.connect(self.onRequestTrainHandler)

    def onRequestTrainHandler(self):
        # 만약 task, step수가 유효하지 않다면 return
        if(self.train_start_clicked() == False): return
        widget.setCurrentIndex(widget.currentIndex() + 1)
        on_layout_convert_center(main_window, widget, 500, 500)


# 제공자 화면 - widget_index_num : 4
class ProviderLayout(ProviderWidget):
    def __init__(self):
        super().__init__()

# 요청자 화면 - widget_index_num : 3
class ReqUserLayout(UserFrameWidget):
    def __init__(self):
        super().__init__()
        self.aten_btn.clicked.connect(self.onProjectCreateHandler)

    def onProjectCreateHandler(self):
        widget.setCurrentIndex(4)
        Prov_ly.onAttendHandler(self.attend_learning())
        print(Prov_ly.self_attend_p_id)
        on_layout_convert_center(main_window, widget, 500, 500)

# 요청자 / 제공자 선택 화면 - widget_index_num : 2
class Mode(ModeChoiceWidget):
    def __init__(self):
        super().__init__()
        self.req_size.clicked.connect(self.openReqUserClass)
        self.shr_size.clicked.connect(self.openProviderClass)

    def openReqUserClass(self):
        #main_window.create_project.setEnabled(True)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        on_layout_convert_center(main_window, widget, 700, 500)

    def openProviderClass(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)
        on_layout_convert_center(main_window, widget, 700, 500)


# 회원가입 화면 - widget_index_num : 1
class SignUp(SignUpWidget):
    def __init__(self):
        super().__init__()
        ## 회원가입
        # 가입완료 버튼눌렀을 경우
        self.sign_submit.clicked.connect(self.onClickSignUpHandler)
        # 돌아가기 버튼 눌렀을 경우
        self.go_back.clicked.connect(self.openLoginClass)
        self.pwd.returnPressed.connect(self.onClickSignUpHandler)
    def onClickSignUpHandler(self):
        result = self.onClickSignUp()
        if(result):
            self.openLoginClass()


    def openLoginClass(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        on_layout_convert_center(main_window, widget, 400, 350)

# 로그인 화면 - widget_index_num : 0
class Login(LoginWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()
        ## 로그인
        # 로그인 버튼 눌렀을 경우
        self.login.clicked.connect(self.onClickLoginHandler)

        # pwd 입력 창에 커서를 두고 엔터 키 눌렀을 시 로그인 할 수 있도록
        self.pwd.returnPressed.connect(self.onClickLoginHandler)

        # 회원가입 버튼 눌렀을 경우우
        self.sign_up.clicked.connect(self.openSignUpClass)

    def openSignUpClass(self):
        # currentIndex를 +- 해주면서 스택 레이아웃 전환
        widget.setCurrentIndex(widget.currentIndex()+1)
        on_layout_convert_center(main_window, widget, 320, 250)

    def onClickLoginHandler(self):
        user_key = self.onClickLogin() # 서버로 로그인 req... 결과로 res["auth"] 리턴
        self.openModeClass()
        main_window.addUserInfoOnToolBar(self.id.text(), "0")

    def openModeClass(self):
        widget.setCurrentIndex(widget.currentIndex()+2)
        on_layout_convert_center(main_window, widget, 450, 250)

class MyMainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowIcon(QIcon('./local_data/daig_icon.png'))

    self.id_lbl = QLabel(self) #
    self.space = QLabel("  ", self)
    self.space_ = QLabel("  ", self)
    self.crdt_lbl = QLabel(self) #

    # 중앙 공백
    self.center_space = QWidget() #
    self.center_space.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #

    # 툴바 아이콘 지정 및 행동 지정
    self.go_home = QAction(QIcon('./local_data/home.png'), 'Home', self)
    self.create_project = QAction(QIcon('./local_data/create.png'), 'New Project', self)
    self.refresh = QAction(QIcon('./local_data/refresh.png'), 'Refresh', self)
    self.go_home.setStatusTip('Home')
    self.go_home.triggered.connect(self.onToolBarTriggeredHandler) # 아이콘 클릭시 mode설정 화면으로 돌아감
    self.toolbar = self.addToolBar('Home')
    self.toolbar.addAction(self.go_home)
    self.toolbar.addAction(self.create_project)
    self.toolbar.addAction(self.refresh)

    self.create_project.triggered.connect(self.openDataUploadClass)
    self.refresh.triggered.connect(User_ly.refresh_learning)
  def openDataUploadClass(self):
      widget.setCurrentIndex(5)
      on_layout_convert_center(self, widget, 500, 500)

    # 로그인 시 툴바에 id와 credit 정보 추가
  def addUserInfoOnToolBar(self, id, credit):
    self.id_lbl.setText("ID : " + id)
    self.crdt_lbl.setText("Credit : " + credit)
    self.toolbar.addWidget(self.center_space) #
    self.toolbar.addWidget(self.id_lbl) #
    self.toolbar.addWidget(self.space)
    self.toolbar.addWidget(self.crdt_lbl) #
    self.toolbar.addWidget(self.space_)

  def toolBarTriggerHandler(self):
    if (widget.currentIndex() < 2 or (widget.currentIndex() > 5 and widget.currentIndex() < 7)):
        self.go_home.setEnabled(False)
    else:
        self.go_home.setEnabled(True)
    if (widget.currentIndex() == 3):
        self.create_project.setEnabled(True)
        self.refresh.setEnabled(True)
    else:
        self.create_project.setEnabled(False)
        self.refresh.setEnabled(False)
    pass

  def onToolBarTriggeredHandler(self):
    widget.setCurrentIndex(2)
    on_layout_convert_center(self, widget, 450, 250)

# don't touch
if __name__ == '__main__':
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #화면 전환용 Widget 설정
    widget = QStackedWidget()

    #레이아웃 인스턴스 생성
    Login_ly = Login()
    SignUp_ly = SignUp()
    Mode_ly = Mode()
    User_ly = ReqUserLayout()
    Prov_ly = ProviderWidget()
    DtUp_ly = DataUploadLayout()
    Progress_ly = Progress()
    TrainRslt_ly = TrainResult()

    #레이아웃 스택 추가
    widget.addWidget(Login_ly)
    widget.addWidget(SignUp_ly)
    widget.addWidget(Mode_ly)
    widget.addWidget(User_ly)
    widget.addWidget(Prov_ly)
    widget.addWidget(DtUp_ly)
    widget.addWidget(Progress_ly)
    #widget.addWidget(TrainRslt_ly)


    #윈도우 객체 생성 및 타이틀 설정
    main_window = MyMainWindow()
    main_window.setWindowTitle("DAIG")

    # 윈도우 크기 설정 -> 화면 중앙 배치 -> 윈도우 열기
    on_layout_convert_center(main_window, widget, 400, 350)
    main_window.toolBarTriggerHandler()
    main_window.show()

    sys.exit(app.exec_())

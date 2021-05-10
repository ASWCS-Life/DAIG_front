import sys
from component.center import *
from login import login
from signUp import sign_up
from mode import modeChoice
from req.auth import *
from userLayout import *
from trainResult import *
from progress import *
from dataUpload import *
from PyQt5.QtWidgets import *

# 학습 결과 화면 - widget_index_num : 7


class TrainResult(train_result):
    def __init__(self):
        super().__init__()
        #self.get_model.clicked.connet(self.openModelInfoHandler)

    def openModelInfoHandler(self):
        return


# 진행 상황 - widget_index_num : 6
class Progress(on_progress):
    def __init__(self):
        super().__init__()
        self.result_btn.clicked.connect(self.openProgressClassHandler)

    def openProgressClassHandler(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        onLayoutConvertCenter(main_window, widget, 700, 500)


# 데이터 업로드 화면 - widget_index_num : 5
class DataUploadLayout(data_upload):
    def __init__(self):
        super().__init__()
        self.train_start.clicked.connect(self.onRequestTrainHandler)

    def onRequestTrainHandler(self):
        # task, step 및 모델, data 파일 반영
        widget.setCurrentIndex(widget.currentIndex() + 1)
        onLayoutConvertCenter(main_window, widget, 800, 500)


# 제공자 화면 - widget_index_num : 4
#class ProviderLayout(proFrame):

# 요청자 화면 - widget_index_num : 3
class ReqUserLayout(userFrame):
    def __init__(self):
        super().__init__()
        self.p_id = self.project_create.clicked.connect(
            self.onProjectCreateHandler)

    def onProjectCreateHandler(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        onLayoutConvertCenter(main_window, widget, 800, 500)

# 요청자 / 제공자 선택 화면 - widget_index_num : 2


class Mode(modeChoice):
    def __init__(self):
        super().__init__()
        self.req_size.clicked.connect(self.openReqUserClass)
        #self.shr_size.clicked.connect(self.openShrUserClass)

    def openReqUserClass(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        onLayoutConvertCenter(main_window, widget, 300, 600)
    #def openShrUserClass(self):


# 회원가입 화면 - widget_index_num : 1
class SignUp(sign_up):
    def __init__(self):
        super().__init__()
        ## 회원가입
        # 가입완료 버튼눌렀을 경우
        self.sign_submit.clicked.connect(self.onClickSignUpHandler)
        # 돌아가기 버튼 눌렀을 경우
        self.go_back.clicked.connect(self.openLoginClass)

    def onClickSignUpHandler(self):
        result = self.onClickSignUp()
        if(result):
            self.openLoginClass()

    def openLoginClass(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        onLayoutConvertCenter(main_window, widget, 300, 300)

# 로그인 화면 - widget_index_num : 0


class Login(login):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()
        ## 로그인
        # 로그인 버튼 눌렀을 경우
        self.login.clicked.connect(self.onClickLoginHandler)
        # 회원가입 버튼 눌렀을 경우우
        self.sign_up.clicked.connect(self.openSignUpClass)

    def openSignUpClass(self):
        # currentIndex를 +- 해주면서 스택 레이아웃 전환
        widget.setCurrentIndex(widget.currentIndex()+1)
        onLayoutConvertCenter(main_window, widget, 200, 200)

    def onClickLoginHandler(self):
        user_key = self.onClickLogin()  # 서버로 로그인 req... 결과로 res["auth"] 리턴
        if(user_key):
            self.openModeClass()
        set_auth_header(user_key)  # 로그인 할때 받은 키로 ({"key" : "~"}) 헤더 설정

    def openModeClass(self):
        widget.setCurrentIndex(widget.currentIndex()+2)
        onLayoutConvertCenter(main_window, widget, 520, 300)


class MyMainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    #self.setCentralWidget(widget)

    # 툴바 아이콘 지정 및 헹동 지정
    self.go_home = QAction(QIcon('./local_data/home.png'), 'Home', self)
    self.go_home.setStatusTip('Home')
    self.go_home.triggered.connect(
        self.onToolBarTriggeredHandler)  # 아이콘 클릭시 mode설정 화면으로 돌아감
    # todo : 다시 되돌아 갔을 때 레이아웃 설정 해줘야함 (design part)

    self.toolbar = self.addToolBar('Home')
    self.toolbar.addAction(self.go_home)

  def toolBarTriggerHandler(self):
    if (widget.currentIndex() < 2 or widget.currentIndex() > 5):
        self.go_home.setEnabled(False)
    else:
        self.go_home.setEnabled(True)

  def onToolBarTriggeredHandler(self):
    widget.setCurrentIndex(2)
    onLayoutConvertCenter(self, widget, 520, 300)


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
    DtUp_ly = DataUploadLayout()
    Progress_ly = Progress()
    TrainRslt_ly = TrainResult()

    #레이아웃 스택 추가
    widget.addWidget(Login_ly)
    widget.addWidget(SignUp_ly)
    widget.addWidget(Mode_ly)
    widget.addWidget(User_ly)
    widget.addWidget(User_ly)  # 나중에 ProviderLayout 으로 교체
    widget.addWidget(DtUp_ly)
    widget.addWidget(Progress_ly)
    widget.addWidget(TrainRslt_ly)

    #윈도우 객체 생성 및 타이틀 설정
    main_window = MyMainWindow()
    main_window.setWindowTitle("DAIG")

    # 윈도우 크기 설정 -> 화면 중앙 배치 -> 윈도우 열기
    onLayoutConvertCenter(main_window, widget, 400, 200)
    main_window.toolBarTriggerHandler()
    main_window.show()

    sys.exit(app.exec_())

import sys
from component.center import *
from login import login
from signUp import sign_up
from mode import modeChoice
from req.auth import *
from userLayout import *
from PyQt5.QtWidgets import QApplication, QStackedWidget

# 요청자 화면 - widget_index_num : 3
class ReqUserLayout(userWindow):
    def __init__(self):
        super().__init__()
        self.p_id = self.user_frame.project_create.clicked.connect(self.user_frame.createProject)
        self.user_frame.project_upload.clicked.connect(lambda: self.user_frame.uploadData(self.p_id))
        self.user_frame.project_start.clicked.connect(lambda: self.user_frame.startProject(self.p_id))
        self.model = self.user_frame.project_result.clicked.connect(lambda: self.user_frame.resultProject(self.p_id))

    #def onProjectCreateHandler(self): return

    #def onProjectUploadHandler(self): return

    #def onProjectStartHandler(self): return

    #def onProjectResultHandler(self): return


# 요청자 / 제공자 선택 화면 - widget_index_num : 2
class Mode(modeChoice):
    def __init__(self):
        super().__init__()
        self.req_size.clicked.connect(self.openReqUserClass)
        #self.shr_size.clicked.connect(self.openShrUserClass)

    def openReqUserClass(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setGeometry(300, 300, 800, 700)

        center(widget)
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
        widget.setGeometry(300, 300, 400, 300)
        center(widget)

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
        widget.setGeometry(300, 300, 520, 300)
        center(widget)

    def onClickLoginHandler(self):
        user_key = self.onClickLogin() # result로
        if(user_key): self.openModeClass()
        set_auth_header(user_key) # user_key로 헤더 설정

    def openModeClass(self):
        widget.setCurrentIndex(widget.currentIndex()+2)
        widget.setGeometry(300,300, 520, 300)
        center(widget)

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

    #레이아웃 스택 추가
    widget.addWidget(Login_ly)
    widget.addWidget(SignUp_ly)
    widget.addWidget(Mode_ly)
    widget.addWidget(User_ly)

    # 창 띄우기 및 중간배치
    widget.setWindowTitle('DAIG')
    widget.setGeometry(300, 300, 300, 300)
    center(widget)
    widget.show()

    sys.exit(app.exec_())

# todo
'''
0. 프로젝트 헤더에 key 값 넣기 ?
1. QWindow 안에 WidgetStack 넣기
2. Grid style로 QWindow를 Widget에 따라 화면 크기 맞추기
'''
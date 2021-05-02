import sys
from center import center
from login import login
from signUp import sign_up
from mode import modeChoice
from PyQt5.QtWidgets import QApplication, QStackedWidget

# 요청자 / 제공자 선택 화면
class Mode(modeChoice):
    def __init__(self):
        super().__init__()
        #self.req_size.clicked.connect(self.openReqUserClass)
        #self.shr_size.clicked.connect(self.openShrUserClass)

    #def openReqUserClass(self):

    #def openShrUserClass(self):


# 회원가입 화면
class SignUp(sign_up):
    def __init__(self):
        super().__init__()
        self.sign_submit.clicked.connect(self.openLoginClass)
        self.go_back.clicked.connect(self.openLoginClass)

    def openLoginClass(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setGeometry(300, 300, 400, 300)
        center(widget)

# 로그인 화면
class Login(login):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()
        # 로그인 누른 후 넘어가기
        self.login.clicked.connect(self.openModeClass)
        self.sign_up.clicked.connect(self.openSignUpClass)

    def openSignUpClass(self):
        # currentIndex를 +- 해주면서 스택 레이아웃 전환
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setGeometry(300, 300, 520, 300)
        center(widget)

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
    login_ly = Login()
    SignUp_ly = SignUp()
    Mode_ly = Mode()

    #레이아웃 스택 추가
    widget.addWidget(login_ly)
    widget.addWidget(SignUp_ly)
    widget.addWidget(Mode_ly)

    # 창 띄우기 및 중간배치
    widget.setWindowTitle('DAIG')
    widget.setGeometry(300, 300, 400, 300)
    center(widget)
    widget.show()


    sys.exit(app.exec_())
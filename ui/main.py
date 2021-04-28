import sys
from signUp import sign_up
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, \
    QLineEdit, QLabel, QStackedWidget

class SignUp(sign_up):
    def __init__(self):
        super().__init__()
        self.sign_submit.clicked.connect(self.openLoginClass)
        self.go_back.clicked.connect(self.openLoginClass)

    def openLoginClass(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setGeometry(300, 300, 400, 300)
        center(widget)

class Login(QWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()
        # 로그인 누른 후 넘어가기
        self.sign_up.clicked.connect(self.openSignUpClass)

    def openSignUpClass(self):
        # currentIndex를 +- 해주면서 스택 레이아웃 전환
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setGeometry(300, 300, 520, 300)
        center(widget)

    # code
    def initUI(self):
        # 로그인 버튼
        self.login = QPushButton('Login', self)
        self.login.resize(80, 80)
        self.login.move(300, 90)

        # 회원가입 버튼
        self.sign_up = QPushButton('회원가입', self)
        self.sign_up.move(150, 180)

        # 아이디, 비밀번호 알리기
        label_id = QLabel('ID', self)
        label_id.move(20, 100)
        font_id = label_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)

        label_pwd = QLabel('Password', self)
        label_pwd.move(20, 140)
        font_pwd = label_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)

        # 아이디, 비밀번호 작성
        self.id = QLineEdit(self)
        self.id.move(90, 100)
        self.pwd = QLineEdit(self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.move(90, 140)

    # 아이디, 비밀번호 창
    def onChanged(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.pwd.setText(text)
        self.pwd.adjustSize()

# 화면 중앙 배치
def center(w):
    qr = w.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    w.move(qr.topLeft())

# don't touch
if __name__ == '__main__':
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #화면 전환용 Widget 설정
    widget = QStackedWidget()

    #레이아웃 인스턴스 생성
    login_ly = Login()
    SignUp_ly = SignUp()

    #레이아웃 스택 추가
    widget.addWidget(login_ly)
    widget.addWidget(SignUp_ly)

    # 창 띄우기 및 중간배치
    widget.setWindowTitle('DAIG')
    widget.setGeometry(300, 300, 400, 300)
    center(widget)
    widget.show()


    sys.exit(app.exec_())
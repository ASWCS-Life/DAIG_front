import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel


class sign_up(QWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()

    # code
    def initUI(self):
    # 가입완료 버튼
        self.sign_submit = QPushButton('가입완료', self)
        self.sign_submit.move(310, 260)

    # 돌아가기 버튼
        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(410, 260)

    # 아이디, 비밀번호, 이름, 이메일 알리기
        sign_id = QLabel('ID', self)
        sign_id.move(20, 55)
        font_id = sign_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)

        sign_pwd = QLabel('Password', self)
        sign_pwd.move(20, 95)
        font_pwd = sign_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)


        sign_name = QLabel('Name', self)
        sign_name.move(20, 135)
        font_pwd = sign_name.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)

        sign_email = QLabel('Email', self)
        sign_email.move(20, 175)
        font_pwd = sign_email.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)

        sign_alpha = QLabel('@', self)
        sign_alpha.move(290, 175)
        font_pwd = sign_alpha.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)

    # 아이디, 비밀번호, 이름, 이메일 작성
        self.id = QLineEdit(self)
        self.id.move(95, 50)

        self.pwd = QLineEdit(self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.move(95, 90)

        self.name = QLineEdit(self)
        self.name.move(95, 130)

        self.email_id = QLineEdit(self)
        self.email_id.move(95, 170)

        self.email_addr = QLineEdit(self)
        self.email_addr.move(310, 170)


    # onChange Handler
    def onChanged(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.pwd.setText(text)
        self.pwd.adjustSize()
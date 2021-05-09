import sys
from PyQt5.QtWidgets import *
from req.rest import *


class login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 로그인 버튼
        self.login = QPushButton('Login', self)
        self.login.resize(80, 80)
        self.login.move(300, 20)

        # 회원가입 버튼
        self.sign_up = QPushButton('회원가입', self)
        self.sign_up.move(150, 110)

        # 아이디, 비밀번호 알리기
        self.label_id = QLabel('ID ', self)
        self.label_id.move(20, 30)
        font_id = self.label_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)

        self.label_pwd = QLabel('Password ', self)
        self.label_pwd.move(20, 70)
        font_pwd = self.label_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)

        # 아이디, 비밀번호 작성
        self.id = QLineEdit(self)
        self.id.move(100, 30)
        self.pwd = QLineEdit(self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.move(100, 70)

    # 아이디, 비밀번호 창
    def onChanged(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.pwd.setText(text)
        self.pwd.adjustSize()

    def onClickLogin(self):
        sender_data = {
           "username" : self.id.text(),
           "password" : self.pwd.text()
        }
        print(sender_data)
        res = login_req(sender_data)
        print(res)
        if(res["is_successful"] == True):
            return res["auth"]
        else:
            QMessageBox.about(self, 'DAIG', res["message"])
            return False

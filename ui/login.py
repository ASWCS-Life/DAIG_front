from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QLineEdit, QLabel
from req.rest import *


class login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

    def onClickLogin(self):
        sender_data = {
           "username" : self.id.text(),
           "password" : self.pwd.text()
        }
        print(sender_data)
        res = post("auth/login", sender_data)
        print(res)
        if(res["is_successful"] == True):
            return True
        else:
            QMessageBox.about(self, 'DAIG', res["message"])
            return False
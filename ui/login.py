import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from daig.api.rest import login_req
from daig.api.auth import set_auth_header
from component.constants import setLabelStyle, setButtonStyle, setLoginButtonStyle, setEditStandard

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Daig 이미지
        daig_img = QPixmap('./local_data/daig_img.png') # 비율 10:4
        self.img_container = QLabel(self)
        self.img_container.setPixmap(QPixmap(daig_img))
        self.img_container.setScaledContents(True)
        self.img_container.setMaximumSize(300, 120)
        self.img_container.move(70, 20)

        # 로그인 버튼
        self.login = QPushButton('Login', self)
        self.login.resize(80, 80)
        self.login.move(300, 170)

        setLoginButtonStyle(self.login)

        # 회원가입 버튼
        self.sign_up = QPushButton('회원가입', self)
        self.sign_up.move(30, 265)
        setButtonStyle(self.sign_up)
        self.sign_up.setFixedWidth(340)

        # 아이디 찾기 버튼
        self.find_id = QPushButton('아이디 찾기', self)
        self.find_id.move(30, 305)
        setButtonStyle(self.find_id)
        self.find_id.setFixedWidth(340)

        # 비밀번호 찾기 버튼
        self.find_pwd = QPushButton('비밀번호 찾기', self)
        self.find_pwd.move(30, 345)
        setButtonStyle(self.find_pwd)
        self.find_pwd.setFixedWidth(340)

        # 아이디, 비밀번호 알리기
        self.label_id = QLabel('ID ', self)
        self.label_id.move(20, 185)
        font_id = self.label_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)
        setLabelStyle(self.label_id)

        self.label_pwd = QLabel('Password ', self)
        self.label_pwd.move(20, 225)
        font_pwd = self.label_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)
        setLabelStyle(self.label_pwd)

        # 아이디, 비밀번호 작성
        self.id = QLineEdit(self)
        self.id.move(100, 180)
        setEditStandard(self.id, 100, 180, '아이디')
        self.id.setFixedWidth(185)

        self.pwd = QLineEdit(self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.move(100, 220)
        self.pwd.setFixedWidth(185)
        setEditStandard(self.pwd, 100, 220, '비밀번호')

    # 아이디, 비밀번호 창
    def on_changed(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.pwd.setText(text)
        self.pwd.adjustSize()

    def on_click_login(self):
        sender_data = {
           "username" : self.id.text(),
           "password" : self.pwd.text()
        }
        print(sender_data)
        res = login_req(sender_data)
        print(res)
        if(res["is_successful"] == True):
            set_auth_header(res["auth"])
            print('set auth')
            return res["auth"]
        else:
            QMessageBox.about(self, 'DAIG', res["message"])
            return False

    def on_clean_line_edit(self):
        self.id.setText("")
        self.pwd.setText("")
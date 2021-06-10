from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QLineEdit, QLabel
from daig.api.rest import sign_up_req
from component.constants import setLabelStyle, setButtonStyle, setEditStandard

class SignUpWidget(QWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()

    # code
    def initUI(self):
    # 가입완료 버튼
        self.sign_submit = QPushButton('가입완료', self)
        self.sign_submit.move(255, 165)
        setButtonStyle(self.sign_submit)

    # 돌아가기 버튼
        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(375, 165)
        setButtonStyle(self.go_back)

    # 이메일 인증 버튼
        self.email = ''
        self.check_email_authorized = False # 이메일 인증 여부
        self.auth_email = QPushButton('인증', self)
        self.auth_email.move(430, 107)
        setButtonStyle(self.auth_email)
        self.auth_email.setFixedWidth(50)
        self.auth_email.clicked.connect(self.email_auth)

    # 아이디, 비밀번호, 이메일 알리기
        sign_id = QLabel('ID', self)
        sign_id.move(20, 35)
        font_id = sign_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)
        setLabelStyle(sign_id)

        sign_pwd = QLabel('Password', self)
        sign_pwd.move(20, 75)
        font_pwd = sign_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)
        setLabelStyle(sign_pwd)

        sign_email = QLabel('Email', self)
        sign_email.move(20, 115)
        font_email = sign_email.font()
        font_email.setBold(True)
        font_email.setPointSize(20)
        setLabelStyle(sign_email)

        alpha = QLabel('@', self)
        alpha.move(248, 113)


    # 아이디, 비밀번호, 이메일 작성
        self.id = QLineEdit(self)
        self.id.setFixedWidth(150)
        setEditStandard(self.id, 95, 30, '아이디')

        self.pwd = QLineEdit(self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setFixedWidth(150)
        setEditStandard(self.pwd, 95, 70, '비밀번호')

        self.email_front = QLineEdit(self)
        self.email_front.setFixedWidth(150)
        setEditStandard(self.email_front, 95, 110, '이메일')

        self.email_back = QLineEdit(self)
        self.email_back.setFixedWidth(150)
        setEditStandard(self.email_back, 265, 110, 'daig.co.kr')
        

    def email_auth(self):

        QMessageBox.about(self,'DAIG',"준비중입니다.")




    # onChange Handler
    def on_changed(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.pwd.setText(text)
        self.pwd.adjustSize()
        self.email_front.setText(text)
        self.email_front.adjustSize()
        self.email_back.setText(text)
        self.email_back.adjustSize()

    def on_click_sign_up(self):
        sender_data = {
           "username" : self.id.text(),
           "password" : self.pwd.text(),
        }
        res = sign_up_req(sender_data)
        if(res["is_successful"] == True):
            QMessageBox.about(self, 'DAIG', res["message"])
            return True
        else:
            QMessageBox.about(self, 'DAIG', res["message"])
            return False
    
    def on_clean_line_edit(self):
        self.id.setText("")
        self.pwd.setText("")
        self.email_front.setText("")
        self.email_back.setText("")
from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QLineEdit, QLabel
from .daig.api.rest import sign_up_req, verify_email, verify_code, verify_username
from .component.constants import set_label_style, set_button_style, set_edit_standard


class SignUpWidget(QWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()

    # code
    def initUI(self):
        self.is_username_available = False
        self.check_email_authorized = False  # 이메일 인증 여부

    # 가입완료 버튼
        self.sign_submit = QPushButton('가입완료', self)
        self.sign_submit.move(255, 205)
        set_button_style(self.sign_submit)

    # 돌아가기 버튼
        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(375, 205)
        set_button_style(self.go_back)

    # 중복 아이디 확인 버튼
        self.code = ''
        self.dup_username = QPushButton('중복확인', self)
        self.dup_username.move(375, 27)
        set_button_style(self.dup_username)
        self.dup_username.clicked.connect(self.check_username)

    # 이메일 인증 버튼
        self.email = ''
        self.send_email = QPushButton('인증하기', self)
        self.send_email.move(375, 107)
        set_button_style(self.send_email)
        self.send_email.clicked.connect(self.check_email)

    # 이메일 인증 버튼
        self.code = ''
        self.auth_code = QPushButton('코드확인', self)
        self.auth_code.move(375, 147)
        set_button_style(self.auth_code)
        self.auth_code.clicked.connect(self.check_code)

    # 아이디, 비밀번호, 이메일 알리기
        sign_id = QLabel('ID', self)
        sign_id.move(20, 35)
        font_id = sign_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)
        set_label_style(sign_id)

        sign_pwd = QLabel('Password', self)
        sign_pwd.move(20, 75)
        font_pwd = sign_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)
        set_label_style(sign_pwd)

        sign_email = QLabel('Email', self)
        sign_email.move(20, 115)
        font_email = sign_email.font()
        font_email.setBold(True)
        font_email.setPointSize(20)
        set_label_style(sign_email)

        sign_code = QLabel('Code', self)
        sign_code.move(20, 155)
        font_code = sign_code.font()
        font_code.setBold(True)
        font_code.setPointSize(20)
        set_label_style(sign_code)

    # 아이디, 비밀번호, 이메일 작성
        self.id = QLineEdit(self)
        self.id.setFixedWidth(150)
        set_edit_standard(self.id, 95, 30, '아이디')

        self.pwd = QLineEdit(self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setFixedWidth(150)
        set_edit_standard(self.pwd, 95, 70, '비밀번호(최소 4자리 이상)')

        self.email = QLineEdit(self)
        self.email.setFixedWidth(220)
        set_edit_standard(self.email, 95, 110, '이메일')

        self.code = QLineEdit(self)
        self.code.setFixedWidth(80)
        set_edit_standard(self.code, 95, 150, '인증 코드')

    # 이메일 인증

    def check_email(self):
        self.check_email_authorized = False
        req_data = {
            'email': self.email.text()
        }
        res_data = verify_email(req_data)
        # if res_data['is_successful']:

        QMessageBox.about(self, 'DAIG', res_data["message"])

    def check_code(self):
        req_data = {
            'email': self.email.text(),
            'code': self.code.text()
        }
        res_data = verify_code(req_data)
        if res_data['is_successful']:
            self.check_email_authorized = True
        QMessageBox.about(self, 'DAIG', res_data["message"])

    def check_username(self):
        self.is_username_available = False
        req_data = {
            'username': self.id.text(),
        }
        res_data = verify_username(req_data)
        if res_data['is_successful']:
            self.is_username_available = True
        QMessageBox.about(self, 'DAIG', res_data["message"])

    def on_changed(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.pwd.setText(text)
        self.pwd.adjustSize()
        self.email_front.setText(text)
        self.email_front.adjustSize()

    def on_click_sign_up(self):
        if(len(self.pwd.text()) < 4):
            QMessageBox.about(self, 'DAIG', '비밀번호가 너무 짧습니다.\n(최소 4자리 이상)')
            return

        if(self.is_username_available == False):
            QMessageBox.about(self, 'DAIG', 'ID 중복확인을 해주세요.')
            return

        if(self.check_email_authorized == False):
            QMessageBox.about(self, 'DAIG', '이메일 인증을 해주세요.')
            return
        sender_data = {
            "username": self.id.text(),
            "password": self.pwd.text(),
            "email": self.email.text()
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
        self.email.setText("")
        self.code.setText("")

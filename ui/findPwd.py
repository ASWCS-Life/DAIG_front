from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit
from .component.constants import set_label_style, set_edit_standard, set_button_style


class FindPwdWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.email = ''

        sign_id = QLabel('ID', self)
        sign_id.move(20, 23)
        font_id = sign_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)
        set_label_style(sign_id)

        sign_email = QLabel('Email', self)
        sign_email.move(20, 53)
        font_email = sign_email.font()
        font_email.setBold(True)
        font_email.setPointSize(20)
        set_label_style(sign_email)

        alpha = QLabel('@', self)
        alpha.move(228, 53)

        self.id = QLineEdit(self)
        self.id.move(100, 180)
        set_edit_standard(self.id, 75, 20, '아이디')
        self.id.setFixedWidth(150)

        self.email_front = QLineEdit(self)
        self.email_front.setFixedWidth(150)
        set_edit_standard(self.email_front, 75, 50, '이메일')

        self.email_back = QLineEdit(self)
        self.email_back.setFixedWidth(150)
        set_edit_standard(self.email_back, 245, 50, 'daig.co.kr')

        self.find_btn = QPushButton('비밀번호 찾기', self)
        self.find_btn.move(165, 90)
        set_button_style(self.find_btn)

        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(285, 90)
        set_button_style(self.go_back)

    def on_changed(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.email_front.setText(text)
        self.email_front.adjustSize()
        self.email_back.setText(text)
        self.email_back.adjustSize()

    def on_user_info_alert(self):
        self.email = self.email_front.text() + '@' + self.email_back.text()

    def on_clean_line_edit(self):
        self.id.setText("")
        self.email_front.setText("")
        self.email_back.setText("")

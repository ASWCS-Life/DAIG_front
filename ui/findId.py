from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from component.constants import set_label_style, set_edit_standard, set_button_style

class FindIdWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.email = ''
        sign_email = QLabel('Email', self)
        sign_email.move(20, 23)
        font_email = sign_email.font()
        font_email.setBold(True)
        font_email.setPointSize(20)
        set_label_style(sign_email)

        alpha = QLabel('@', self)
        alpha.move(228, 23)

        self.email_front = QLineEdit(self)
        self.email_front.setFixedWidth(150)
        set_edit_standard(self.email_front, 75, 20, '이메일')

        self.email_back = QLineEdit(self)
        self.email_back.setFixedWidth(150)
        set_edit_standard(self.email_back, 245, 20, 'daig.co.kr')

        self.find_btn = QPushButton('아이디 찾기', self)
        self.find_btn.move(165, 60)
        set_button_style(self.find_btn)

        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(285, 60)
        set_button_style(self.go_back)

    def on_changed(self, text):
        self.email_front.setText(text)
        self.id.adjustSize()
        self.email_back.setText(text)
        self.pwd.adjustSize()

    def on_email_alert(self):
        self.email = self.email_front.text() + '@' + self.email_back

    def on_clean_line_edit(self):
        self.email_front.setText("")
        self.email_back.setText("")
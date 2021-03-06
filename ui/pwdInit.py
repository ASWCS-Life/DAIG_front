from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from .component.constants import set_label_style, set_edit_standard, set_button_style


class PwdInitWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        sign_pwd = QLabel('비밀번호 입력', self)
        sign_pwd.move(20, 23)
        font_pwd = sign_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)
        set_label_style(sign_pwd)

        check_pwd = QLabel('비밀번호 확인', self)
        check_pwd.move(20, 53)
        font_check = check_pwd.font()
        font_check.setBold(True)
        font_check.setPointSize(20)
        set_label_style(check_pwd)

        self.pwd = QLineEdit(self)
        self.pwd.move(100, 180)
        self.pwd.setEchoMode(QLineEdit.Password)
        set_edit_standard(self.pwd, 150, 20, '비밀번호')
        self.pwd.setFixedWidth(200)

        self.check_pwd = QLineEdit(self)
        self.check_pwd.setFixedWidth(200)
        self.check_pwd.setEchoMode(QLineEdit.Password)
        set_edit_standard(self.check_pwd, 150, 50, '한번 더 입력')

        self.pwd_init_btn = QPushButton('비밀번호 변경', self)
        self.pwd_init_btn.move(120, 90)
        set_button_style(self.pwd_init_btn)

        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(240, 90)
        set_button_style(self.go_back)

    def on_changed(self, text):
        self.pwd.setText(text)
        self.pwd.adjustSize()
        self.check_pwd.setText(text)
        self.check_pwd.adjustSize()

    def on_pwd_init_alert(self):
        if(self.pwd.text() != self.check_pwd.text()):
            QMessageBox.about(self, 'DAIG', '비밀번호가 서로 일치하지 않습니다.')
        pass

    def on_clean_line_edit(self):
        self.check_pwd.setText("")
        self.pwd.setText("")

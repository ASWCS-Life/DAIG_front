from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QPushButton, QLineEdit
from .component.constants import set_label_style, set_edit_standard, set_button_style
from .daig.api.rest import find_id


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

        self.email = QLineEdit(self)
        self.email.setFixedWidth(150)
        set_edit_standard(self.email, 75, 20, '이메일')

        self.find_btn = QPushButton('아이디 찾기', self)
        self.find_btn.move(165, 60)
        self.find_btn.clicked.connect(self.find_btn_clicked)
        set_button_style(self.find_btn)

        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(285, 60)
        set_button_style(self.go_back)

    
    def find_btn_clicked(self):
        res_data=find_id(self.email.text())
        QMessageBox.about(self, 'DAIG', res_data["message"])
    

    def on_clean_line_edit(self):
        self.email.setText("")

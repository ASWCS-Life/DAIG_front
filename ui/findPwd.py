from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from component.constants import setLabelStyle, setEditStandard, setButtonStyle

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
        setLabelStyle(sign_id)

        sign_email = QLabel('Email', self)
        sign_email.move(20, 53)
        font_email = sign_email.font()
        font_email.setBold(True)
        font_email.setPointSize(20)
        setLabelStyle(sign_email)

        alpha = QLabel('@', self)
        alpha.move(228, 53)

        self.id = QLineEdit(self)
        self.id.move(100, 180)
        setEditStandard(self.id, 75, 20, '아이디')
        self.id.setFixedWidth(150)

        self.email_front = QLineEdit(self)
        self.email_front.setFixedWidth(150)
        setEditStandard(self.email_front, 75, 50, '이메일')

        self.email_back = QLineEdit(self)
        self.email_back.setFixedWidth(150)
        setEditStandard(self.email_back, 245, 50, 'daig.co.kr')

        self.find_btn = QPushButton('비밀번호 찾기', self)
        self.find_btn.move(165, 90)
        setButtonStyle(self.find_btn)

        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(285, 90)
        setButtonStyle(self.go_back)

    def onChanged(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.email_front.setText(text)
        self.email_front.adjustSize()
        self.email_back.setText(text)
        self.email_back.adjustSize()

    def onUserInfoAlert(self):
        self.email = self.email_front.text() + '@' + self.email_back.text()

        #-----   self.id.text() & self.email 로 해당 아이디및 이메일에 해당하는 정보가 있는지에 대한 요청
        # res[is_successful] == True면 비밀번호 변경화면 레이아웃으로 이동하게 만듬
        # response에 헤더를 받아와서 비밀번호 변경할때 해당 헤더를 사용해야 할듯해요

        # if (res["is_successful"] == True):
        #    QMessageBox.about(self, 'DAIG', res['message'])
        #    return True
        # else:
        #    QMessageBox.about(self, 'DAIG', res['message'])
        #    return False
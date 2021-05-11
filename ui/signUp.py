from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QLineEdit, QLabel
from daig.api.rest import sign_up_req

class SignUpWidget(QWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()

    # code
    def initUI(self):
    # 가입완료 버튼
        self.sign_submit = QPushButton('가입완료', self)
        self.sign_submit.move(95, 150)

    # 돌아가기 버튼
        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(195, 150)

    # 아이디, 비밀번호, 이름, 이메일 알리기
        sign_id = QLabel('ID', self)
        sign_id.move(20, 35)
        font_id = sign_id.font()
        font_id.setBold(True)
        font_id.setPointSize(20)

        sign_pwd = QLabel('Password', self)
        sign_pwd.move(20, 75)
        font_pwd = sign_pwd.font()
        font_pwd.setBold(True)
        font_pwd.setPointSize(20)


    # 아이디, 비밀번호, 이름, 이메일 작성
        self.id = QLineEdit(self)
        self.id.move(95, 30)

        self.pwd = QLineEdit(self)
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.move(95, 70)


    # onChange Handler
    def onChanged(self, text):
        self.id.setText(text)
        self.id.adjustSize()
        self.pwd.setText(text)
        self.pwd.adjustSize()

    def onClickSignUp(self):
        sender_data = {
           "username" : self.id.text(),
           "password" : self.pwd.text()
        }
        res = sign_up_req(sender_data)
        if(res["is_successful"] == True):
            QMessageBox.about(self, 'DAIG', res["message"])
            return True
        else:
            QMessageBox.about(self, 'DAIG', res["message"])
            return False
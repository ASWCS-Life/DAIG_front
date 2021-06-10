from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from component.constants import setLabelStyle, setEditStandard, setButtonStyle

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
        setLabelStyle(sign_pwd)

        check_pwd = QLabel('비밀번호 확인', self)
        check_pwd.move(20, 53)
        font_check = check_pwd.font()
        font_check.setBold(True)
        font_check.setPointSize(20)
        setLabelStyle(check_pwd)

        self.pwd = QLineEdit(self)
        self.pwd.move(100, 180)
        self.pwd.setEchoMode(QLineEdit.Password)
        setEditStandard(self.pwd, 150, 20, '비밀번호')
        self.pwd.setFixedWidth(200)

        self.check_pwd = QLineEdit(self)
        self.check_pwd.setFixedWidth(200)
        self.check_pwd.setEchoMode(QLineEdit.Password)
        setEditStandard(self.check_pwd, 150, 50, '한번 더 입력')

        self.pwd_init_btn = QPushButton('비밀번호 변경', self)
        self.pwd_init_btn.move(120, 90)
        setButtonStyle(self.pwd_init_btn)

        self.go_back = QPushButton('돌아가기', self)
        self.go_back.move(240, 90)
        setButtonStyle(self.go_back)

    def on_changed(self, text):
        self.pwd.setText(text)
        self.pwd.adjustSize()
        self.check_pwd.setText(text)
        self.check_pwdt.adjustSize()

    def on_pwd_init_alert(self):
        if(self.pwd.text() != self.check_pwd.text()):
            QMessageBox.about(self, 'DAIG', '비밀번호가 서로 일치하지 않습니다.')
        pass
        # -----   self.pwd.text() 로 비밀번호 변경 요청
        #
        # res[is_successful] == True면 비밀번호 변경화면 레이아웃으로 이동하게 만듬

        # res["is_successful"] == True 면 다시 로그인 화면으로 돌아가도록 해놓음
        # if (res["is_successful"] == True):
        #    QMessageBox.about(self, 'DAIG', res['message'])
        #    return True
        # else:
        #    QMessageBox.about(self, 'DAIG', res['message'])
        #    return False

    def on_clean_line_edit(self):
        self.check_pwd.setText("")
        self.pwd.setText("")
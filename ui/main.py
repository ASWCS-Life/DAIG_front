import sys
from PyQt5.QtWidgets import QSizePolicy,QWidget, QLabel,QMainWindow, QApplication, QStackedWidget, QAction
from PyQt5.QtGui import QIcon
from component.constants import enterPressedHandler
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSlot

from component.center import on_layout_convert_center

from pwdInit import PwdInitWidget
from findPwd import FindPwdWidget
from findId import FindIdWidget
from login import LoginWidget
from signUp import SignUpWidget
from mode import ModeChoiceWidget
from userLayout import UserFrameWidget
from providerLayout import ProviderWidget
from trainResult import TrainResultWidget
from progress import ProgressWidget
from dataUpload import DataUploadWidget
from breakdown import BrDownWidget
from credit import CreditWidget
from creditWebView import WebViewWidget
from daig.api.rest import get_current_credit


#11
class WebViewLayout(WebViewWidget):
    def __init__(self):
        super().__init__()

#10
class BrDownLayout(BrDownWidget):
    def __init__(self):
        super().__init__()

#9
class CreditLayout(CreditWidget):
    def __init__(self):
        super().__init__()
        self.all_btn.clicked.connect(self.openBrDownClass)
        self.dep_btn.clicked.connect(self.openWebViewClass)

    def openBrDownClass(self):
        self.all_btn_clicked()
        widget.setCurrentIndex(10)
        BrDown_ly.reqUserBreakDown()
        on_layout_convert_center(main_window, widget, 400, 500)

    def openWebViewClass(self):
        self.dep_btn_clicked()
        widget.setCurrentIndex(11)
        on_layout_convert_center(main_window, widget, 600, 500)
#8
class PwdInitLayout(PwdInitWidget):
    def __init__(self):
        super().__init__()

        self.pwd_init_btn.clicked.connect(self.onPwdInitHandler)
        self.go_back.clicked.connect(self.openFindPwdClass)
        enterPressedHandler(self.pwd, self.onPwdInitHandler)
        enterPressedHandler(self.check_pwd, self.onPwdInitHandler)

    def onPwdInitHandler(self):
        if(self.onPwdInitAlert() == True):
            widget.setCurrentIndex(0)
            on_layout_convert_center(main_window, widget, 420, 180)

    def openFindPwdClass(self):
        widget.setCurrentIndex(7)
        on_layout_convert_center(main_window, widget, 420, 180)

# 비밀번호 찾기 화면 - widget_index_num : 7
class FindPwdLayout(FindPwdWidget):
    def __init__(self):
        super().__init__()
        self.find_btn.clicked.connect(self.onFindPwdHandler)
        self.go_back.clicked.connect(self.openLoginClass)
        enterPressedHandler(self.id, self.onFindPwdHandler)
        enterPressedHandler(self.email_front, self.onFindPwdHandler)
        enterPressedHandler(self.email_back, self.onFindPwdHandler)

    def onFindPwdHandler(self):
        if(self.onUserInfoAlert() == True):
            widget.setCurrentIndex(8)
            on_layout_convert_center(main_window, widget, 370, 180)

    def openLoginClass(self):
        widget.setCurrentIndex(0)
        on_layout_convert_center(main_window, widget, 400, 430)

# 아이디 찾기 화면 - widget_index_num : 6
class FindIdLayout(FindIdWidget):
    def __init__(self):
        super().__init__()
        self.find_btn.clicked.connect(self.onFindIdHandler)
        self.go_back.clicked.connect(self.openLoginClass)
        enterPressedHandler(self.email_front, self.onFindIdHandler)
        enterPressedHandler(self.email_back, self.onFindIdHandler)

    def onFindIdHandler(self):
        if(self.onEmailAlert() == True):
            widget.setCurrentIndex(0)
            on_layout_convert_center(main_window, widget, 420, 180)

    def openLoginClass(self):
        widget.setCurrentIndex(0)
        on_layout_convert_center(main_window, widget, 400, 430)

# 데이터 업로드 화면 - widget_index_num : 5
class DataUploadLayout(DataUploadWidget):
    def __init__(self):
        super().__init__()

    def complete_upload(self):
    # 성공적으로 프로젝트가 생성되면
        widget.setCurrentIndex(3)
        on_layout_convert_center(main_window, widget, 700, 500)

# 제공자 화면 - widget_index_num : 4
class ProviderLayout(ProviderWidget):
    def __init__(self):
        super().__init__()

# 요청자 화면 - widget_index_num : 3
class ReqUserLayout(UserFrameWidget):
    def __init__(self):
        super().__init__()
        self.aten_btn.clicked.connect(self.onProjectCreateHandler)

    def onProjectCreateHandler(self):
        widget.setCurrentIndex(4)
        Prov_ly.onAttendHandler(self.attend_learning()) # 요청자가 프로젝트에 참여버튼을 누르면 제공자에 해당 p_id 전송
        print(Prov_ly.self_attend_p_id)
        on_layout_convert_center(main_window, widget, 700, 500)

# 요청자 / 제공자 모드 선택 화면 - widget_index_num : 2
class Mode(ModeChoiceWidget):
    def __init__(self):
        super().__init__()
        self.req_size.clicked.connect(self.openReqUserClass)
        self.shr_size.clicked.connect(self.openProviderClass)

    def openReqUserClass(self):
        #main_window.create_project.setEnabled(True)
        widget.setCurrentIndex(3)
        on_layout_convert_center(main_window, widget, 700, 500)

    def openProviderClass(self):
        widget.setCurrentIndex(4)
        on_layout_convert_center(main_window, widget, 700, 500)


# 회원가입 화면 - widget_index_num : 1
class SignUp(SignUpWidget):
    def __init__(self):
        super().__init__()
        ## 회원가입
        # 가입완료 버튼눌렀을 경우
        self.sign_submit.clicked.connect(self.onClickSignUpHandler)
        # 돌아가기 버튼 눌렀을 경우
        self.go_back.clicked.connect(self.openLoginClass)
        self.pwd.returnPressed.connect(self.onClickSignUpHandler)

        # enter 키 눌렀을 때의 동작
        enterPressedHandler(self.id, self.onClickSignUpHandler) ######
        enterPressedHandler(self.pwd, self.onClickSignUpHandler) ######
        enterPressedHandler(self.email_front, self.onClickSignUpHandler) ####
        enterPressedHandler(self.email_back, self.onClickSignUpHandler) #####
    def onClickSignUpHandler(self):
        result = self.onClickSignUp()
        if(result):
            self.openLoginClass()


    def openLoginClass(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        on_layout_convert_center(main_window, widget, 400, 430) ##########

# 로그인 화면 - widget_index_num : 0
class Login(LoginWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()
        ## 로그인
        # 로그인 버튼 눌렀을 경우
        self.login.clicked.connect(self.onClickLoginHandler)

        # id, pwd 입력 창에 커서를 두고 엔터 키 눌렀을 시 로그인 할 수 있도록
        # self.pwd.returnPressed.connect(self.onClickLoginHandler)
        enterPressedHandler(self.id, self.onClickLoginHandler) #####
        enterPressedHandler(self.pwd, self.onClickLoginHandler)# ####

        # 회원가입 버튼 눌렀을 경우
        self.sign_up.clicked.connect(self.openSignUpClass)
        # 아이디 찾기 눌렀을 경우
        self.find_id.clicked.connect(self.openFindIdClass)
        # 비밀번호 찾기 눌렀을 경우
        self.find_pwd.clicked.connect(self.openFindPwdClass)

    def openFindPwdClass(self):
        widget.setCurrentIndex(7)
        on_layout_convert_center(main_window, widget, 420, 180)

    def openFindIdClass(self):
        widget.setCurrentIndex(6)
        on_layout_convert_center(main_window, widget, 420, 150)

    def openSignUpClass(self):
        widget.setCurrentIndex(1)
        on_layout_convert_center(main_window, widget, 500, 250)

    def onClickLoginHandler(self):
        user_key = self.onClickLogin() # 서버로 로그인 req... 결과로 res["auth"] 리턴
        self.openModeClass()
        main_window.addUserInfoOnToolBar(self.id.text(), "0")

    def openModeClass(self):
        widget.setCurrentIndex(2)
        WebView_ly = WebViewLayout()
        widget.addWidget(WebView_ly)  # 11
        on_layout_convert_center(main_window, widget, 450, 250)

class MyMainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowIcon(QIcon('./local_data/daig_icon.png'))

    self.id_lbl = QLabel(self) #
    self.space = QLabel("  ", self)
    self.space_ = QLabel("  ", self)
    self.crdt_lbl = QLabel(self) #

    # 중앙 공백
    self.center_space = QWidget() #
    self.center_space.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #

    # 툴바 아이콘 지정 및 행동 지정
    self.go_home = QAction(QIcon('./local_data/home.png'), 'Home', self)
    self.create_project = QAction(QIcon('./local_data/create.png'), 'New Project', self)
    self.credit = QAction(QIcon('./local_data/credit.png'), 'Credit Info', self)
    self.go_home.setStatusTip('Home')
    self.go_home.triggered.connect(self.onToolBarTriggeredHandler) # 아이콘 클릭시 mode설정 화면으로 돌아감
    self.toolbar = self.addToolBar('Home')
    self.toolbar.addAction(self.go_home)
    self.toolbar.addAction(self.create_project)
    self.toolbar.addAction(self.credit)

    self.create_project.triggered.connect(self.openDataUploadClass)
    self.credit.triggered.connect(self.onCreditTriggeredHandler)
  def openDataUploadClass(self):
      widget.setCurrentIndex(5)
      on_layout_convert_center(self, widget, 500, 500)

    # 로그인 시 툴바에 id와 credit 정보 추가
  def addUserInfoOnToolBar(self, id, credit):
    res_data=get_current_credit()
    self.id_lbl.setText(f'ID : {res_data["id"]}')
    self.crdt_lbl.setText(f'Credit : {res_data["credit"]}')
    self.toolbar.addWidget(self.center_space) #
    self.toolbar.addWidget(self.id_lbl) #
    self.toolbar.addWidget(self.space)
    self.toolbar.addWidget(self.crdt_lbl) #
    self.toolbar.addWidget(self.space_)

  def toolBarTriggerHandler(self):
    if (widget.currentIndex() < 2 or (widget.currentIndex() > 5 and widget.currentIndex() < 9)):
        self.go_home.setEnabled(False)
        self.credit.setEnabled(False)
    else:
        self.go_home.setEnabled(True)
        self.credit.setEnabled(True)
    if (widget.currentIndex() == 3):
        self.create_project.setEnabled(True)
    else:
        self.create_project.setEnabled(False)
    pass

  def onToolBarTriggeredHandler(self):
    widget.setCurrentIndex(2)
    on_layout_convert_center(self, widget, 450, 250)
  def onCreditTriggeredHandler(self):
    widget.setCurrentIndex(9)
    res_data = get_current_credit()
    Credit_ly.credit_amount = f'Credit : {res_data["credit"]}'
    on_layout_convert_center(self, widget, 400, 300)
# don't touch
if __name__ == '__main__':
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #화면 전환용 Widget 설정
    widget = QStackedWidget()

    #레이아웃 인스턴스 생성
    Login_ly = Login()
    SignUp_ly = SignUp()
    Mode_ly = Mode()
    User_ly = ReqUserLayout()
    Prov_ly = ProviderLayout()
    DtUp_ly = DataUploadLayout()
    FdId_ly = FindIdLayout()
    FdPwd_ly = FindPwdLayout()
    PwdInit_ly = PwdInitLayout()
    Credit_ly = CreditLayout()
    BrDown_ly = BrDownLayout()
    
    #Progress_ly = Progress()
    #TrainRslt_ly = TrainResult()

    #레이아웃 스택 추가
    widget.addWidget(Login_ly) #0
    widget.addWidget(SignUp_ly) #1
    widget.addWidget(Mode_ly) #2
    widget.addWidget(User_ly) #3
    widget.addWidget(Prov_ly) #4
    widget.addWidget(DtUp_ly) #5
    widget.addWidget(FdId_ly) #6
    widget.addWidget(FdPwd_ly) #7
    widget.addWidget(PwdInit_ly) #8
    widget.addWidget(Credit_ly)  # 9
    widget.addWidget(BrDown_ly)  # 10
    
    #widget.addWidget(Progress_ly) - 진행상황 ui 따로 필요 x (요청자 화면에서 진행상황을 보여줄 것임)
    #widget.addWidget(TrainRslt_ly) - 결과확인 ui 따로 필요 x (결과 모델을 따로 다운받을 수 있도록)


    #윈도우 객체 생성 및 타이틀 설정
    main_window = MyMainWindow()
    main_window.setWindowTitle("DAIG")

    # 윈도우 크기 설정 -> 화면 중앙 배치 -> 윈도우 열기
    on_layout_convert_center(main_window, widget, 400, 430) ##########
    main_window.toolBarTriggerHandler()
    main_window.show()

    sys.exit(app.exec_())

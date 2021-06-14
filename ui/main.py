import sys
from PyQt5.QtWidgets import QSizePolicy,QWidget, QLabel,QMainWindow, QApplication, QStackedWidget, QAction
from PyQt5.QtGui import QIcon
from component.constants import enter_pressed_handler
from component.center import on_layout_convert_center

from pwdInit import PwdInitWidget
from findPwd import FindPwdWidget
from findId import FindIdWidget
from login import LoginWidget
from signUp import SignUpWidget
from mode import ModeChoiceWidget
from userLayout import UserFrameWidget
from providerLayout import ProviderWidget
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
        self.all_btn.clicked.connect(self.open_br_down_class)
        self.dep_btn.clicked.connect(self.open_web_view_class)
        self.refresh.clicked.connect(self.on_refresh_button)

    def open_br_down_class(self):
        widget.setCurrentIndex(10)
        widget.currentWidget().call_credit_log()
        on_layout_convert_center(main_window, widget, 400, 500)

    def open_web_view_class(self):
        self.dep_btn_clicked()
        widget.setCurrentIndex(11)
        on_layout_convert_center(main_window, widget, 930, 650)

    def on_refresh_button(self):
        self.on_refresh_handler()
        res = get_current_credit()
        main_window.crdt_lbl.setText(f'Credit : {res["credit"]}')

        
#8
class PwdInitLayout(PwdInitWidget):
    def __init__(self):
        super().__init__()

        self.pwd_init_btn.clicked.connect(self.on_pwd_init_handler)
        self.go_back.clicked.connect(self.open_find_pwd_class)
        enter_pressed_handler(self.pwd, self.on_pwd_init_handler)
        enter_pressed_handler(self.check_pwd, self.on_pwd_init_handler)

    def on_pwd_init_handler(self):
        if(self.on_pwd_init_alert() == True):
            widget.setCurrentIndex(0)
            on_layout_convert_center(main_window, widget, 420, 180)

    def open_find_pwd_class(self):
        widget.setCurrentIndex(7)
        on_layout_convert_center(main_window, widget, 420, 180)

# 비밀번호 찾기 화면 - widget_index_num : 7
class FindPwdLayout(FindPwdWidget):
    def __init__(self):
        super().__init__()
        self.find_btn.clicked.connect(self.on_find_pwd_handler)
        self.go_back.clicked.connect(self.open_login_class)
        enter_pressed_handler(self.id, self.on_find_pwd_handler)

    def on_find_pwd_handler(self):
        if(self.on_user_info_alert() == True):
            widget.setCurrentIndex(8)
            widget.currentWidget().on_clean_line_edit()
            on_layout_convert_center(main_window, widget, 370, 180)

    def open_login_class(self):
        widget.setCurrentIndex(0)
        on_layout_convert_center(main_window, widget, 400, 430)

# 아이디 찾기 화면 - widget_index_num : 6
class FindIdLayout(FindIdWidget):
    def __init__(self):
        super().__init__()
        self.find_btn.clicked.connect(self.on_find_id_handler)
        self.go_back.clicked.connect(self.open_login_class)

    def on_find_id_handler(self):
        if(self.on_email_alert() == True):
            widget.setCurrentIndex(0)
            on_layout_convert_center(main_window, widget, 420, 180)

    def open_login_class(self):
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
        self.aten_btn.clicked.connect(self.on_project_create_handler)

    def on_project_create_handler(self):
        widget.setCurrentIndex(4)
        Prov_ly.on_attend_handler(self.attend_learning())
        print(Prov_ly.self_attend_p_id)
        on_layout_convert_center(main_window, widget, 700, 500)

# 요청자 / 제공자 모드 선택 화면 - widget_index_num : 2
class Mode(ModeChoiceWidget):
    def __init__(self):
        super().__init__()
        self.req_size.clicked.connect(self.open_req_user_class)
        self.shr_size.clicked.connect(self.open_provider_class)

    def open_req_user_class(self):
        widget.setCurrentIndex(3)
        on_layout_convert_center(main_window, widget, 700, 500)

    def open_provider_class(self):
        widget.setCurrentIndex(4)
        on_layout_convert_center(main_window, widget, 700, 500)



# 회원가입 화면 - widget_index_num : 1
class SignUp(SignUpWidget):
    def __init__(self):
        super().__init__()

        self.sign_submit.clicked.connect(self.on_click_sign_up_handler)
        self.go_back.clicked.connect(self.open_login_class)
        self.pwd.returnPressed.connect(self.on_click_sign_up_handler)

    def on_click_sign_up_handler(self):
        result = self.on_click_sign_up()
        if(result):
            self.open_login_class()


    def open_login_class(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        on_layout_convert_center(main_window, widget, 400, 430)

# 로그인 화면 - widget_index_num : 0
class Login(LoginWidget):
    # don't touch
    def __init__(self):
        super().__init__()
        self.initUI()
        ## 로그인
        # 로그인 버튼 눌렀을 경우
        self.login.clicked.connect(self.on_click_login_handler)

        enter_pressed_handler(self.id, self.on_click_login_handler) #####
        enter_pressed_handler(self.pwd, self.on_click_login_handler)# ####

        # 회원가입 버튼 눌렀을 경우
        self.sign_up.clicked.connect(self.open_sign_up_class)
        # 아이디 찾기 눌렀을 경우
        self.find_id.clicked.connect(self.open_find_id_class)
        # 비밀번호 찾기 눌렀을 경우
        self.find_pwd.clicked.connect(self.open_find_pwd_class)

    def open_find_pwd_class(self):
        widget.setCurrentIndex(7)
        widget.currentWidget().on_clean_line_edit()
        on_layout_convert_center(main_window, widget, 420, 180)

    def open_find_id_class(self):
        widget.setCurrentIndex(6)
        widget.currentWidget().on_clean_line_edit()
        on_layout_convert_center(main_window, widget, 420, 150)

    def open_sign_up_class(self):
        widget.setCurrentIndex(1)
        widget.currentWidget().on_clean_line_edit()
        on_layout_convert_center(main_window, widget, 500, 300)

    def on_click_login_handler(self):
        self.on_click_login() # 서버로 로그인 req... 결과로 res["auth"] 리턴
        self.open_mode_class()
        main_window.add_user_info_on_tool_bar()

    def open_mode_class(self):
        widget.setCurrentIndex(2)
        Credit_ly = CreditLayout()
        BrDown_ly = BrDownLayout()
        WebView_ly = WebViewLayout()
        widget.addWidget(Credit_ly)  # 9
        widget.addWidget(BrDown_ly)  # 10
        widget.addWidget(WebView_ly)  # 11
        res_data = get_current_credit()
        Credit_ly.credit_amount = str(res_data["credit"])
        # 여기서 크레딧페이지 생성
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
    self.go_home.triggered.connect(self.on_tool_bar_triggered_handler) # 아이콘 클릭시 mode설정 화면으로 돌아감
    self.toolbar = self.addToolBar('Home')
    self.toolbar.addAction(self.go_home)
    self.toolbar.addAction(self.create_project)
    self.toolbar.addAction(self.credit)

    self.create_project.triggered.connect(self.open_data_upload_class)
    self.credit.triggered.connect(self.on_credit_triggered_handler)
  def open_data_upload_class(self):
      widget.setCurrentIndex(5)
      widget.currentWidget().on_clean_line_edit()
      on_layout_convert_center(self, widget, 500, 500)

    # 로그인 시 툴바에 id와 credit 정보 추가
  def add_user_info_on_tool_bar(self):
    res_data=get_current_credit()
    self.id_lbl.setText(f'ID : {res_data["id"]}')
    self.crdt_lbl.setText(f'Credit : {res_data["credit"]}')
    self.toolbar.addWidget(self.center_space) #
    self.toolbar.addWidget(self.id_lbl) #
    self.toolbar.addWidget(self.space)
    self.toolbar.addWidget(self.crdt_lbl) #
    self.toolbar.addWidget(self.space_)

  def tool_bar_trigger_handler(self):
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

  def on_tool_bar_triggered_handler(self):
    widget.setCurrentIndex(2)
    on_layout_convert_center(self, widget, 450, 250)
  def on_credit_triggered_handler(self):
    widget.setCurrentIndex(9)
    on_layout_convert_center(self, widget, 600, 500)
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


    #윈도우 객체 생성 및 타이틀 설정
    main_window = MyMainWindow()
    main_window.setWindowTitle("DAIG")

    # 윈도우 크기 설정 -> 화면 중앙 배치 -> 윈도우 열기
    on_layout_convert_center(main_window, widget, 400, 430)
    main_window.tool_bar_trigger_handler()
    main_window.show()

    sys.exit(app.exec_())

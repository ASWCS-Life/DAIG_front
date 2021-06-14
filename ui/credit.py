from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from component.constants import set_big_button_style
from daig.api.rest import get_current_credit


class CreditWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.init_ui()

  def init_ui(self):

    res = get_current_credit()
    self.credit_amount = str(res["credit"])
    self.label = QLabel(self.credit_amount + '원', self) 
    self.label.setAlignment(Qt.AlignCenter)
    self.label_font = self.label.font()
    self.label_font.setPointSize(25)
    self.label_font.setBold(True)
    self.label.setFont(self.label_font)

  # 크레딧 충전 버튼
    self.dep_btn = QPushButton('크레딧 충전', self)
    self.dep_btn.setFont(QFont('맑은 고딕', 12))
    set_big_button_style(self.dep_btn)

  # 내역 확인 버튼
    self.all_btn = QPushButton('내역 확인', self)
    self.all_btn.setFont(QFont('맑은 고딕', 12))
    set_big_button_style(self.all_btn)

  # 새로 고침 버튼
    self.refresh = QPushButton('새로 고침', self)
    self.refresh.setFont(QFont('맑은 고딕', 12))
    set_big_button_style(self.refresh)

  # 레이아웃 설정
    layout = QGridLayout()
    layout.addWidget(self.label, 1, 0, -1, 1)
    layout.addWidget(self.dep_btn, 1, 1)
    layout.addWidget(self.all_btn, 2, 1)
    layout.addWidget(self.refresh, 3, 1)
    self.setLayout(layout)

  # 내역확인 눌렀을 시
  def all_btn_clicked(self):
    pass


  # 출금하기 눌렀을 시
  def dep_btn_clicked(self):
    pass

  # 새로고침 버튼 눌렀을 시
  def on_refresh_handler(self):
    res = get_current_credit()
    self.credit_amount = str(res["credit"])
    self.label.setText(self.credit_amount + '원') 
    pass

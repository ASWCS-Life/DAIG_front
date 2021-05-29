from PyQt5.QtWidgets import *
from daig.api.rest import get_credit_log

class BrDownWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.init_ui()

  def init_ui(self):
    self.formLayout = QFormLayout()
    self.formLayout.setSpacing(20)
    groupBox = QGroupBox()
    #groupBox.setStyleSheet()

    self.p_date = []

    creditLog_list=get_credit_log()
    print('loglist: ')
    print(creditLog_list[0])
    # dummy
    for i in range(len(creditLog_list)):
      self.p_date.append(QLabel('  ' + '날짜: ' + creditLog_list[i]["date"] + '  +'+ str(creditLog_list[i]["amount"]) + '원' ))
      self.formLayout.addRow(self.p_date[i])
      self.p_date[i].setStyleSheet('border: 1px solid #FFB914;'
                              'font-size: 18px;'
                              'font-family: 맑은 고딕;'
                              'border-radius: 5px')

    groupBox.setLayout(self.formLayout)
    scroll = QScrollArea()
    scroll.setWidget(groupBox)
    scroll.setWidgetResizable(True)
    scroll.setFixedHeight(400)
    scroll.setStyleSheet("QScrollBar:vertical {border: none;"
                         "background: white;"
                         "width: 5px;}"
                         )

    layout = QVBoxLayout(self)
    layout.addWidget(scroll)

  # BrDownWidget이 트리거 될때마다 내역 불러오기
  def reqUserBreakDown(self):
      self.p_date = []

      # ------ 내역 호출
      # list = res["list"]
      #for i in range(len(list)):
          #self.p_date.append(QLabel('  ' + 'list[i]["date"]' + '\t\t\t\t' + 'list[i]["amount"]' + ' '))
          #self.formLayout.addRow(self.p_date[i])
          #self.p_date[i].setStyleSheet('border: 1px solid #FFB914;'
          #                             'font-size: 18px;'
          #                             'font-family: 맑은 고딕;'
          #                             'border-radius: 5px')

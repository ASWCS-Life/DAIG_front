from PyQt5.QtWidgets import *
from component.constants import setLabelStyle, setButtonStyle, setLoginButtonStyle
from tensorflow import keras

class UserFrameWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):
    # tab바
    self.pro_tab = QWidget()
    self.cre_tab = QWidget()

    self.tabs = QTabWidget()
    self.tabs.addTab(self.pro_tab, 'Project')
    self.tabs.addTab(self.cre_tab, 'Credit')

    # 프로젝트 테이블 바
    self.pro_tab.layout = QVBoxLayout()
    self.pro_table = QTableWidget()
    self.pro_table.setColumnCount(3)  # column 설정
    self.pro_table.setHorizontalHeaderLabels(['Project 이름(id)', '진행도', '비고'])

    # test
    self.p_id = '123'
    self.prog = '12/13'
    self.remark = '정상'

    # 테이블 전체 너비와 컨텐츠들의 비율에 따라 자동으로 컬럼 너비 조정
    project_header = self.pro_table.horizontalHeader()
    twidth = project_header.width()
    width = []
    for column in range(project_header.count()):
      project_header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
      width.append(project_header.sectionSize(column))
    wfactor = twidth / sum(width)
    for column in range(project_header.count()):
      project_header.setSectionResizeMode(column, QHeaderView.Interactive)
      project_header.resizeSection(column, width[column] * wfactor)

    self.pro_tab.layout.addWidget(self.pro_table)
    self.pro_tab.setLayout(self.pro_tab.layout)

    # 크레딧 테이블 바
    self.cre_tab.layout = QVBoxLayout()
    self.cre_table = QTableWidget()
    self.cre_table.setColumnCount(3)
    self.cre_table.setHorizontalHeaderLabels(['날짜', '변동 내역', '상세 내용'])

    # 테이블 크기 정렬
    credit_header = self.cre_table.horizontalHeader()
    twidth = credit_header.width()
    width = []
    for column in range(credit_header.count()):
      credit_header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
      width.append(credit_header.sectionSize(column))
    wfactor = twidth / sum(width)
    for column in range(credit_header.count()):
      credit_header.setSectionResizeMode(column, QHeaderView.Interactive)
      credit_header.resizeSection(column, width[column] * wfactor)

    self.cre_tab.layout.addWidget(self.cre_table)
    self.cre_tab.setLayout(self.cre_tab.layout)

    # 버튼 생성
    self.aten_btn = QPushButton('참여')
    self.stop_btn = QPushButton('중단')
    self.down_btn = QPushButton('다운로드')
    self.get_btn = QPushButton('add_test')


    self.aten_btn.clicked.connect(self.attend_learning)
    self.stop_btn.clicked.connect(self.stop_learning)
    self.down_btn.clicked.connect(self.download_model)

    setButtonStyle(self.aten_btn)
    setButtonStyle(self.stop_btn)
    setButtonStyle(self.down_btn)
    setButtonStyle(self.get_btn)

    #test
    self.get_btn.clicked.connect(lambda: self.project_addItem(self.p_id,
                                                              self.prog,
                                                              self.remark))

    layout = QGridLayout()
    layout.addWidget(self.tabs, 0, 0, 1, 0)
    layout.addWidget(self.aten_btn, 1, 1)
    layout.addWidget(self.stop_btn, 1, 2)
    layout.addWidget(self.down_btn, 1, 3)
    layout.addWidget(self.get_btn, 1, 4)

    self.setLayout(layout)

    # 프로젝트 테이블 동적 생성

  def project_addItem(self, p_id, progression, remark):
    row = self.pro_table.rowCount()
    self.pro_table.insertRow(row)
    self.pro_table.setItem(row, 0, QTableWidgetItem(p_id))
    self.pro_table.setItem(row, 1, QTableWidgetItem(progression))
    self.pro_table.setItem(row, 2, QTableWidgetItem(remark))
    '''
    # json 형식의 res 데이터에 진행중인 프로젝트 정보가 여러개 올때 -> 받아오는 파라미터를 변경해줘야함
    for item in res:
      row = self.pro_table.rowCount() 출력
      self.pro_table.insertRow(row)
      self.pro_table.setItem(row, 0, QTableWidgetItem(item['p_id']))
      self.pro_table.setItem(row, 1, QTableWidgetItem(item['progression']))
      self.pro_table.setItem(row, 2, QTableWidgetItem(item['remark']))

    '''
    pass

  # 크레딧 테이블 동적 생성
  def credit_addItem(self, date, change_info, remark):
    row = self.pro_table.rowCount()
    self.cre_table.insertRow(row)
    self.cre_table.setItem(row, 0, QTableWidgetItem(date))
    self.cre_table.setItem(row, 1, QTableWidgetItem(change_info))
    self.cre_table.setItem(row, 2, QTableWidgetItem(remark))
    '''
    # json 형식의 res 데이터에 진행중인 프로젝트 정보가 여러개 올때 -> 받아오는 파라미터를 변경해줘야함
    for item in res:
      row = self.pro_table.rowCount()
      self.pro_table.insertRow(row)
      self.pro_table.setItem(row, 0, QTableWidgetItem(item['data']))
      self.pro_table.setItem(row, 1, QTableWidgetItem(item['change_info']))
      self.pro_table.setItem(row, 2, QTableWidgetItem(item['remark']))

    '''
    pass

  # 현재 선택한(focus 되어 있는)프로젝트 참여
  def attend_learning(self):
    #if[이미 끝난 프로젝트 라면]:
    #QMessageBox.about(self, 'DAIG', res['message'])
    #return
    return self.pro_table.item(self.pro_table.currentRow(), 0).text()

  def refresh_learning(self):
    print("refresh_button_pressed")
    #if[Toolbar의 refresh button을 눌렀을때]
    #---------- 프로젝트 정보 재요청
    pass

  # 현재 선택한 프로젝트 중단
  def stop_learning(self):
    # self.pro_table.item(self.pro_table.currentRow(), 0).text() # 선택된 열의 p_id를 반환
    # ------ 해당 프로젝트 중단 요청
    pass

  # 현재 선택한 모델 다운로드
  def download_model(self):
    # if[해당 프로젝트가 끝나지 않았으면]
    #   QMessageBox.about(self, 'DAIG', res["message"])

    # self.pro_table.item(self.pro_table.currentRow(), 0).text() # 선택된 열의 p_id를 반환
    # ----- 해당 프로젝트 결과 요청
    # model = 결과 모델

    # 저장할 원하는 파일 이름으로 결과 모델 저장
    file_save = QFileDialog.getSaveFileName(self, 'Save File', './', filter='*.h5')
    file_save_path = file_save[0]
    # model.save(file_save_path)

    pass




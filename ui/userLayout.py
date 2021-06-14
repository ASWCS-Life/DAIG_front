from PyQt5.QtWidgets import *
from .component.constants import set_button_style

from .daig.api.rest import get_owned_projects, result_learning

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


    # 프로젝트 테이블 바
    self.pro_tab.layout = QGridLayout()
    self.pro_table = QTableWidget()
    self.pro_table.setColumnCount(4)  # column 설정
    self.pro_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.pro_table.setHorizontalHeaderLabels(['Project 이름(id)', '진행도', '생성 날짜', '비고'])
    self.pro_table.horizontalHeader().setStyleSheet("QHeaderView::section{"
                                                    'background-color: white;'
                                                    'border: 1px solid rgb(251, 86, 7);'
                                                    'border-radius: 2px;'
                                                    "}")
    self.pro_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.pro_table.setSelectionMode(QAbstractItemView.SingleSelection)

    # test
    self.p_id = '123'
    self.prog = '12/13'
    self.accum_time = '493'
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

    self.pro_tab.layout.addWidget(self.pro_table,0,0,4,5)
    self.pro_tab.setLayout(self.pro_tab.layout)

   
    # 테이블 크기 정렬
    # credit_header = self.cre_table.horizontalHeader()
    # twidth = credit_header.width()
    # width = []
    # for column in range(credit_header.count()):
    #   credit_header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
    #   width.append(credit_header.sectionSize(column))
    # wfactor = twidth / sum(width)
    # for column in range(credit_header.count()):
    #   credit_header.setSectionResizeMode(column, QHeaderView.Interactive)
    #   credit_header.resizeSection(column, width[column] * wfactor)

    # self.cre_tab.layout.addWidget(self.cre_table,0,0,4,5)
    # self.cre_tab.setLayout(self.cre_tab.layout)

    # self.credit_get_btn = QPushButton('새로 고침') # 임시

    # self.cre_tab.layout.addWidget(self.credit_get_btn, 5, 4)

    self.down_btn = QPushButton('다운로드')
    self.get_btn = QPushButton('새로 고침')

    self.down_btn.setEnabled(False) #

    self.down_btn.clicked.connect(self.download_model)

    set_button_style(self.down_btn)
    set_button_style(self.get_btn)

    #test
    self.get_btn.clicked.connect(self.get_projects)

    layout = QGridLayout()
    layout.addWidget(self.tabs, 0, 0, 1, 0)
    #self.pro_tab.layout.addWidget(self.aten_btn, 5, 1)
    #self.pro_tab.layout.addWidget(self.stop_btn, 5, 2)
    self.pro_tab.layout.addWidget(self.down_btn, 5, 3)
    self.pro_tab.layout.addWidget(self.get_btn, 5, 4)
    

    self.setLayout(layout)

    # 프로젝트 테이블 동적 생성

  def project_addItem(self, p_id, progression, accum_time,remark):
    row = self.pro_table.rowCount()
    self.pro_table.insertRow(row)
    self.pro_table.setItem(row, 0, QTableWidgetItem(p_id))
    self.pro_table.setItem(row, 1, QTableWidgetItem(progression))
    self.pro_table.setItem(row, 2, QTableWidgetItem(accum_time)) # 단위는 sec으로 가정
    self.pro_table.setItem(row, 3, QTableWidgetItem(remark))

  def get_projects(self):
    self.pro_table.setRowCount(0)
    projects=get_owned_projects()["projects"]
    for p in projects:
      self.down_btn.setEnabled(True) #
      self.project_addItem(p["project_uid"],p["progress"],p["created_at"],p["status"])


  # 현재 선택한 모델 다운로드
  def download_model(self):
    if(len(self.pro_table.selectedItems()) < 1): return #
    project_id=self.pro_table.selectedItems()[0].text()
    model=result_learning(project_id)
    file_save = QFileDialog.getSaveFileName(self, 'Save File', './', filter='*.h5')
    file_save_path = file_save[0]
    model.save(file_save_path)

    




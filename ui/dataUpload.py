import tensorflow as tf
from .daig.api.rest import *
from PyQt5.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton, QComboBox, QGridLayout, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from .daig.requester import project
from .component.constants import set_label_style, set_button_style, set_edit_standard
import numpy as np
import math
import requests
from tempfile import TemporaryFile
from .daig.api.auth import get_auth_header

class UploadThread(QThread):
  stop_learning = False
  pbar_signal=pyqtSignal(dict)

  def __init__(self,auth, parent=None):
    super(UploadThread, self).__init__(parent)
    self.auth=auth
    print(auth)
    self.model_path=parent.model_path.text()
    self.train_lbl_path=parent.train_lbl_path.text()
    self.train_img_path=parent.train_img_path.text()
    self.task_num = int(parent.cho_task.text())
    self.step_num = int(parent.cho_step.text())
    self.epoch = int(parent.cho_epoch.text())
    self.batch_size = int(parent.cho_batch.text())
    self.contributor = int(parent.cho_contributor.text())
    self.valid_rate = float(parent.cho_valid.text())

  def run(self):
    print(self.model_path)
    try:
      model = tf.keras.models.load_model(self.model_path)
    except:
      QMessageBox.about(self, 'DAIG', '잘못된 h5 모델 파일입니다.')
      return

    res = self.create_project(model.get_weights(), data = {
        'total_task' : self.task_num,
        'step_size' : self.step_num,
        'epoch': self.epoch,
        'batch_size': self.batch_size,
        'valid_rate': self.valid_rate,
        'max_contributor': self.contributor,
        'parameter_number': np.sum([np.prod(v.get_shape().as_list()) for v in model.trainable_variables])
    })

    project.uid=res["project_uid"]

    self.upload_model(self.model_path,project.uid)
    self.upload_data(self.train_img_path,self.train_lbl_path,project.uid,self.task_num)
    

  def create_project(self,initial_weight,data=None):
    with TemporaryFile() as tf:
      np.save(tf, np.array(initial_weight,dtype=object))
      _ = tf.seek(0)
      res = requests.post(f'{base_url}/project/create/', files={'weight':tf},data=data, headers={'AUTH':self.auth})

    return res.json()

  def upload_model(self, model_path, project_uid):
    res=requests.post(f'{base_url}/project/model/upload',data={ # 업로드 url 요청
      'project_uid':project_uid,
      'model':'model.h5'
    }, headers={'AUTH':self.auth})
    print(res.json())

    url=res.json()['model_url'] # presigned url

    with open(model_path, 'rb') as f:
      requests.put(url=url,data=f) # 데이터 업로드
        
    print('model successfully uploaded')

  def upload_each_data(self,data, label, project_uid, idx):
    res=requests.post(f'{base_url}/project/data/upload',data={ # 업로드 url 요청
      'project_uid':project_uid,
      'data': f'train_data_{idx}',
      'label': f'train_label_{idx}',
      'index': idx
    }, headers={'AUTH':self.auth})

    url=res.json()['label_url'] # presigned url
    with TemporaryFile() as tf:
      np.save(tf, label)
      _ = tf.seek(0)
      requests.put(url=url,data=tf) # 라벨 업로드

    url=res.json()['data_url'] # presigned url
    with TemporaryFile() as tf:
      np.save(tf, data)
      _ = tf.seek(0)
      requests.put(url=url,data=tf) # 데이터 업로드

  def upload_data(self,data_path,label_path,project_uid,task_num):
    data=np.load(data_path, allow_pickle=True)
    label=np.load(label_path, allow_pickle=True)
    try:
      data_split=np.split(data,task_num)
      label_split=np.split(label,task_num)
    except:
      QMessageBox.about(self, 'DAIG', '잘못된 npy 데이터 파일입니다.')
      return

    pbar_rate=0
    r=math.floor(10000/task_num)*0.01
    for idx in range(task_num):
      self.upload_each_data(data_split[idx], label_split[idx], project_uid, idx)
      pbar_rate+=r
      self.pbar_signal.emit({
        "is_completed":False,
        "num":pbar_rate
      })
      print(f'{idx} uploaded')
    self.pbar_signal.emit({
      "is_completed":True,
      "num":100
    })
    print('data uploading finished')
    requests.post(f'{base_url}/project/{project_uid}/start/', data={}, headers = {'AUTH' : get_auth_header()})
    

class DataUploadWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):

    # 파일 이름 출력
    self.model = QLabel('model')
    self.train_img = QLabel('train image')
    self.train_lbl = QLabel('train label')
    #self.valid_img = QLabel('valid image')
    #self.valid_lbl = QLabel('valid label')
    self.p_contributer = QLabel('max contributer : ')
    self.p_task_div = QLabel('Task 분할 개수')
    self.p_step_task = QLabel('Step별 task 개수')
    self.p_epoch = QLabel('Epoch number')
    self.p_batch = QLabel('Batch size')
    self.p_contributor = QLabel('최대 참여자수')
    self.p_valid = QLabel('검증 비율')
    self.model_path = QLabel('')
    self.model_path.setMinimumSize(250, 20)
    self.train_img_path = QLabel('')
    self.train_lbl_path = QLabel('')
    #self.valid_img_path = QLabel('')
    #self.valid_lbl_path = QLabel('')

    set_label_style(self.model)
    set_label_style(self.train_img)
    set_label_style(self.train_lbl)
    set_label_style(self.p_task_div)
    set_label_style(self.p_step_task)
    set_label_style(self.p_epoch)
    set_label_style(self.p_batch)
    set_label_style(self.p_contributor)
    set_label_style(self.p_valid)

  # 파일 올리는 버튼
    self.model_btn = QPushButton('올리기')
    self.model_btn.clicked.connect(self.model_btn_clicked)
    self.train_img_btn = QPushButton('올리기')
    self.train_img_btn.clicked.connect(self.train_img_btn_clicked)
    self.train_lbl_btn = QPushButton('올리기')
    self.train_lbl_btn.clicked.connect(self.train_lbl_btn_clicked)
    #self.valid_img_btn = QPushButton('올리기')
    #self.valid_img_btn.clicked.connect(self.train_img_btn_clicked)
    #self.valid_img_btn = QPushButton('올리기')
    #self.valid_img_btn.clicked.connect(self.train_lbl_btn_cliked)

    set_button_style(self.model_btn)
    set_button_style(self.train_img_btn)
    set_button_style(self.train_lbl_btn)

 # task 분할 개수 출력
    self.cho_task = QLineEdit(self)
    set_edit_standard(self.cho_task, 0, 0, 'task num')

  # step별 task 개수
    self.cho_step = QLineEdit(self)
    set_edit_standard(self.cho_step, 0, 0, 'step num')

  # epoch 정보
    self.cho_epoch = QLineEdit(self)
    set_edit_standard(self.cho_epoch, 0, 0, 'epoch')

  # mini batch 정보
    self.cho_batch = QLineEdit(self)
    set_edit_standard(self.cho_batch, 0, 0, 'batch size')

  # 참여자수 정보
    self.cho_contributor = QLineEdit(self)
    set_edit_standard(self.cho_contributor, 0, 0, 'max contributor')

  # 검증 데이터 비율
    self.cho_valid = QLineEdit(self)
    set_edit_standard(self.cho_valid, 0, 0, 'validation split')

  # 학습 시작 버튼
    self.train_start = QPushButton('프로젝트 생성')
    self.train_start.clicked.connect(self.train_start_clicked)
    set_button_style(self.train_start)

    # progress bar
    self.pbar=QProgressBar()

    # 레이아웃 설정 및 출력
    layout = QGridLayout()
    layout.addWidget(self.model, 0, 0)
    layout.addWidget(self.model_path, 0, 1)
    layout.addWidget(self.model_btn, 0, 2)
    layout.addWidget(self.train_img, 1, 0)
    layout.addWidget(self.train_img_path, 1, 1)
    layout.addWidget(self.train_img_btn, 1, 2)
    layout.addWidget(self.train_lbl, 2, 0)
    layout.addWidget(self.train_lbl_path, 2, 1)
    layout.addWidget(self.train_lbl_btn, 2, 2)
    layout.addWidget(self.p_task_div, 3, 0)
    layout.addWidget(self.cho_task, 3, 2)
    layout.addWidget(self.p_step_task, 4, 0)
    layout.addWidget(self.cho_step, 4, 2)
    layout.addWidget(self.p_epoch, 5, 0)
    layout.addWidget(self.cho_epoch, 5, 2)
    layout.addWidget(self.p_batch, 6, 0)
    layout.addWidget(self.cho_batch, 6, 2)
    layout.addWidget(self.p_contributor, 7, 0)
    layout.addWidget(self.cho_contributor, 7, 2)
    layout.addWidget(self.p_valid, 8, 0)
    layout.addWidget(self.cho_valid, 8, 2)
    
    layout.addWidget(self.train_start, 9, 2)
    layout.addWidget(self.pbar, 9, 0, 1, 2)

    self.setLayout(layout)

  # task 분할 개수 출력
  def onChanged(self, text):
    self.cho_task.setText(text)
    self.id.adjustSize()
    self.cho_step.setText(text)
    self.pwd.adjustSize()

  # 모델 파일 받아오기 / 하나의 디렉토리로 받아옵니다. Tensorflow Model Format 참조
  def model_btn_clicked(self):
    self.m_file = QFileDialog.getOpenFileName(self, './', filter="*.h5")
    self.model_path.setText(self.m_file[0])

  # train img 파일 받아오기
  def train_img_btn_clicked(self):
    self.train_img_file = QFileDialog.getOpenFileName(
        self, './', filter="*.npy")
    self.train_img_path.setText(self.train_img_file[0])

  # train lbl 파일 받아오기
  def train_lbl_btn_clicked(self):
    self.train_lbl_file = QFileDialog.getOpenFileName(
        self, './', filter="*.npy")
    self.train_lbl_path.setText(self.train_lbl_file[0])
  

  def train_start_clicked(self):

    error = self.input_format_check()
    if error:
      QMessageBox.about(self, 'DAIG', error)
      return

    self.train_start.setEnabled(False)
    self.upload_thread=UploadThread(get_auth_header(),self)
    self.upload_thread.pbar_signal.connect(self.update_pbar)

    self.upload_thread.start()
    return

  @pyqtSlot(dict)
  def update_pbar(self, content):
    is_completed=content["is_completed"]
    value=content["num"]
    self.pbar.setValue(value)
    if is_completed:
      self.complete_upload()

  def complete_upload(self):
    raise NotImplementedError

  def input_format_check(self):
    if(not (self.cho_task.text().isdecimal() and self.isInt(self.cho_task.text()))):
      return "총 task 크기는 양의 정수형으로 입력해주세요"
    if(not (self.cho_step.text().isdecimal() and self.isInt(self.cho_step.text()))):
      return "step의 크기는 양의 정수형으로 입력해주세요"
    if(not (self.cho_epoch.text().isdecimal() and self.isInt(self.cho_epoch.text()))):
      return "epoch 값은 양의 정수형으로 입력해주세요"
    if(not (self.cho_batch.text().isdecimal() and self.isInt(self.cho_batch.text()))):
      return "batch size는 양의 정수형으로 입력해주세요"
    if(not (self.cho_contributor.text().isdecimal() and self.isInt(self.cho_contributor.text()))):
      return "참여자 수는 양의 정수형으로 입력해주세요"
    if(not (float(self.cho_valid.text()) < 1 and float(self.cho_valid.text()) > 0)):
      return "검증 비율은 0에서 1사이의 실수여야 합니다."
    if(not (self.cho_task.text().isdecimal() and (int(self.cho_task.text()) >= 10 and int(self.cho_task.text()) <= 500))):
      return "task의 숫자가 너무 크거나 작습니다. (10 ~ 500)"
    if(int(self.cho_step.text()) < 1 or int(self.cho_step.text()) > 20):
      return "step의 숫자가 너무 크거나 작습니다. (1 ~ 20)"
    if(int(self.cho_contributor.text()) < 1):
      return "최대 참여자 수는 양의 정수여야 합니다."
    if(int(self.cho_contributor.text()) > int(self.cho_step.text())):
      return "최대 참여자 수는 step size를 넘길 수 없습니다."
    if(int(self.cho_task.text()) % int(self.cho_step.text()) != 0):
      return "총 Task 갯수는 step size로 나누어 떨어질 수 있어야 합니다."

    return False

  def isInt(self, str):
    if(float(str)%1 != 0):
      return False
    else:
      return True
    
  def on_clean_line_edit(self):
    self.cho_batch.setText("")
    self.cho_task.setText("")
    self.cho_step.setText("")
    self.cho_contributor.setText("")
    self.cho_epoch.setText("")
    self.cho_valid.setText("")
    self.model_path.setText("")
    self.train_lbl_path.setText("")
    self.train_img_path.setText("")
    self.pbar.setValue(0)
    self.train_start.setEnabled(True)


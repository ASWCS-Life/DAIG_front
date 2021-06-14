from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from component.constants import set_label_style, set_button_style

class ModeChoiceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 파일 객체 생성
        req_pic = QPixmap('./local_data/user.png')
        shr_pic = QPixmap('./local_data/cloud.png')

    # 이미지 설정
        self.req_img = QLabel(self)
        self.req_img.setMaximumSize(113, 100)
        self.req_img.setMinimumSize(113, 100)
        self.req_img.setPixmap(QPixmap(req_pic))
        self.req_img.setScaledContents(True)
        self.req_size = QPushButton('학습 요청자')

        set_label_style(self.req_img)
        set_button_style(self.req_size)

        self.shr_img = QLabel(self)
        self.shr_img.setMaximumSize(100, 115)
        self.shr_img.setMinimumSize(100, 115)
        self.shr_img.setPixmap(QPixmap(shr_pic))
        self.shr_img.setScaledContents(True)
        self.shr_size = QPushButton('리소스 제공자')

        set_button_style(self.shr_size)

    # 레이아웃 생성 및 배치
        layout = QGridLayout()
        layout.addWidget(self.req_img, 0, 0)
        layout.addWidget(self.req_size, 1, 0)
        layout.addWidget(self.shr_img, 0, 1)
        layout.addWidget(self.shr_size, 1, 1)
        self.setLayout(layout)

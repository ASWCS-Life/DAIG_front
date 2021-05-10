from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap

class ModeChoiceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
    # 파일 객체 생성
        req_pic = QPixmap('./local_data/requester.png')
        req_pic = req_pic.scaledToHeight(200)
        req_pic = req_pic.scaledToWidth(200)

        shr_pic = QPixmap('./local_data/sharing.png')
        shr_pic = shr_pic.scaledToHeight(200)
        shr_pic = shr_pic.scaledToWidth(200)

    # 이미지 설정
        req_img = QLabel()
        req_img.resize(200, 200)
        req_img.setPixmap(req_pic)
        self.req_size = QPushButton('학습 요청자')
        self.req_size.setGeometry(100, 100, 300, 200)


        shr_img = QLabel()
        shr_img.resize(200, 200)
        shr_img.setPixmap(shr_pic)
        self.shr_size = QPushButton('리소스 제공자')
        self.shr_size.move(200, 300)

    # 레이아웃 생성 및 배치
        layout = QGridLayout()
        layout.addWidget(req_img, 0, 0)
        layout.addWidget(self.req_size, 1, 0)
        layout.addWidget(shr_img, 0, 1)
        layout.addWidget(self.shr_size, 1, 1)
        self.setLayout(layout)
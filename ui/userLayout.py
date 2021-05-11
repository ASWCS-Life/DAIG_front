from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QGroupBox, QLabel

class UserFrameWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):
    self.project_create = QPushButton('프로젝트 생성')
  # 사용자 페이지
    grid = QGridLayout()
    grid.addWidget(self.show_user(), 0, 0)
    grid.addWidget(self.project_create, 1, 0)

    self.setLayout(grid)

  def show_user(self):
    user_box = QGroupBox('사용자 프로필')
    user_id = QLabel('ID')
    user_credit = QLabel('Credit')

    user_layout = QHBoxLayout()
    user_layout.addWidget(user_id)
    user_layout.addWidget(user_credit)
    user_box.setLayout(user_layout)

    return user_box




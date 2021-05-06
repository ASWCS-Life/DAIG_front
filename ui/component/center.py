from PyQt5.QtWidgets import QDesktopWidget

# 화면 중앙 배치
def center(w):
    qr = w.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    w.move(qr.topLeft())
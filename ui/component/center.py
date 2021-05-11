from PyQt5.QtWidgets import QDesktopWidget

# 화면 중앙 배치
def on_layout_convert_center(win, wid, x, y):
    win.toolBarTriggerHandler()
    win.setGeometry(300, 300, x, y)
    win.setCentralWidget(wid)
    qr = win.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    win.move(qr.topLeft())
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import sys
import webbrowser
class WebViewWidget(QWidget):
  # don't touch
  def __init__(self):
    super().__init__()
    self.init_ui()

  # code
  def init_ui(self):
      self.web_widget = QLabel(self)
      self.web_widget.setScaledContents(True)
      #self.widget_List.append(self.widget_youtube)
      self.web_widget.setGeometry(QRect(10, 10, 500,
                                        300))  # self.widget_youtube.setStyleSheet("background-color: rgb(84, 84, 84);")
      self.web_widget.setObjectName("widget_youtube")
      self.webview = QWebEngineView(self.web_widget)
      self.webview.setUrl(QUrl("http://127.0.0.1:8000"))
      self.webview.setGeometry(0,0,500,300)


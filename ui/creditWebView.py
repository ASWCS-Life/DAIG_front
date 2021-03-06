from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from .daig.api.auth import get_auth_header

class WebViewWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.get_req_specify()

    def get_req_specify(self):
        print("start")
        auth=get_auth_header()

        baseUrl = 'http://118.67.130.33:8000/credit/payment/' # dummy
        self.req = QWebEngineHttpRequest(url=QUrl(baseUrl))
        self.req.setHeader(QByteArray().append('AUTH'), QByteArray().append(auth)) # dummy
        print(self.req)
        self.load(self.req)

    def reload(self): self.load(self.req)

    def printLoadStart(self): print("Start Loading")

    def printLoading(self): print("Loading")

    def printLoadFinished(self): print("Load Finished")

    def urlChangedFunction(self):
        self.setText(self.toString())
        print("Url Changed")

    def btnBackFunc(self):
        self.back()

    def btnForwardFunc(self):
        self.forward()

    def btnRelaodFunc(self):
        self.reload()

    def btnStopFunc(self):
        self.stop()
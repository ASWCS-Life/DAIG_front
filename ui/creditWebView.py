from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

import sys
import webbrowser
class WebViewWidget(QWebEngineView):
    def __init__(self):
        super().__init__()

        self.setUrl(QUrl("http://127.0.0.1:8000"))
        self.loadStarted.connect(self.printLoadStart)
        self.loadProgress.connect(self.printLoading)
        self.loadFinished.connect(self.printLoadFinished)

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
        
    

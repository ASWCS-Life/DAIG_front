from PyQt5.QtWidgets import QMessageBox
import requests
import ctypes

def response_alert(code):
    if code not in [200, 201, 270, 204] :
        ctypes.windll.user32.MessageBoxW(0, "ALERT", "API response Error!\nProgram terminating ...", 1)
        raise SystemExit(requests.exceptions.HTTPError)
    pass
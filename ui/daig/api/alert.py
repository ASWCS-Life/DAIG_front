from PyQt5.QtWidgets import QMessageBox
import requests

def response_alert(code):
    if code not in [200, 201, 204] :
        QMessageBox.about('DAIG', "API response Error!\nProgram terminating ...")
        raise SystemExit(requests.exceptions.HTTPError)
    pass
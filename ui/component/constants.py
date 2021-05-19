num_of_prgs = 0

def setLoginButtonStyle(lg):
    lg.setStyleSheet('color: white;'
                     'background-color: rgb(251, 86, 7);'
                     'border-radius: 20px;')

def setButtonStyle(bt):
    bt.setFixedSize(110, 30)
    bt.setStyleSheet("QPushButton"
                     "{"
                     'color: rgb(251, 86, 7);'
                     'background-color: white;'
                     'border: 1px solid rgb(251, 86, 7);'
                     'border-radius: 3px;'
                     "}"
                     "QPushButton::pressed"
                     "{"
                     'color: rgb(251, 86, 7);'
                     'background-color: white;'
                     'border: 1px solid rgb(123, 207, 146);'
                     'border-radius: 3px;'
                     "}"
                     "QPushButton::disabled"
                     "{"
                     'color: gray;'
                     'background-color: white;'
                     'border: gray;'
                     'border-radius: 3px;'
                     "}"
                     )

def setLabelStyle(lb):
    lb.setStyleSheet('color: rgb(251, 86, 7)')

# 엔터 눌렀을 때의 동작
def enterPressedHandler(edit, action):
    edit.returnPressed.connect(action)

# lineEdit 기본설정
def setEditStandard(edit ,x_val, y_val, place_holder):
    if(x_val > 0): edit.move(x_val, y_val)
    edit.setPlaceholderText(place_holder)
    edit.setStyleSheet('border: 1px solid gray;'
                       'border-radius: 5px')

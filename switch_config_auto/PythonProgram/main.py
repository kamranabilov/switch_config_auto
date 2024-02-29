

import sys
import serial.tools.list_ports
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QLineEdit, QVBoxLayout,
                             QGridLayout
                             )
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import subprocess
import pyautogui
import time
import pyperclip
import win32gui
import win32con
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import win32functions

com_number = "COM1"
commands = ""


def ready_putty():
    app = Application(backend='uia').start('putty.exe').connect(title='PuTTY Configuration', timeout=100)
    # app.PuttyConfiguration.print_control_identifiers()
    serial = app.PuttyConfiguration.child_window(title="Serial", auto_id="1050",
                                                 control_type="RadioButton").wrapper_object()
    serial.click()
    serialline = app.PuttyConfiguration.child_window(title="Serial line", auto_id="1044",
                                                     control_type="Edit").wrapper_object()
    serialline.type_keys('{DELETE  4}')
    serialline.type_keys(com_number)
    open = app.PuttyConfiguration.child_window(title="Open", auto_id="1009", control_type="Button")
    open.click()
    app2 = Application(backend='uia').connect(title='PuTTY', timeout=3)
    app2.Putty.type_keys('{ENTER}')
    app3 = Application(backend='uia').connect(title=f"{com_number} - PuTTY", timeout=3)
    window_title = f"{com_number.title()}Putty"
    window1 = getattr(app3, window_title)
    #window1.type_keys('{ENTER}')
    window1.type_keys('admin@huawei.com')
    window1.type_keys('{ENTER}')
    window1.type_keys('admin@huawei.com')
    window1.type_keys('{ENTER}')
    time.sleep(10)
    window1.click_input(button='right')
    #window1.maximize()

def find_com_ports():
    global com_number
    ports = serial.tools.list_ports.comports()
    for port in ports:
        #print(f"COM port found: {port.device}")
        com_number=port.device

def config_file(self):
    global commands
    commands = f"""
    system-view
    sysname {self.input1.text()}
    vlan batch {self.input2.text()}
    vlan {self.input2.text()}
    name MANAGEMENT
    quit
    stelnet server enable
    aaa
    local-user miaadmin password irreversible-cipher Admin12345@ 
    local-user miaadmin privilege level 3
    y  
    local-user miaadmin service-type telnet terminal ssh
    quit
    int vlanif {self.input2.text()}
    ip address {self.input3.text()} {self.input5.text()}
    quit
    port-group group-member Ge 1/0/1 to Ge 1/0/8
    port link-type access
    port default vlan {self.input2.text()}  
    quit
    interface 10GE1/0/1
    port link-type trunk
    port trunk allow-pass vlan {self.input2.text()}
    quit
    interface 10GE1/0/2
    port link-type trunk
    port trunk allow-pass vlan {self.input2.text()}
    quit
    interface 10GE1/0/3
    port link-type access
    port default vlan {self.input2.text()}
    quit
    interface 10GE1/0/4
    port link-type access
    port default vlan {self.input2.text()}
    quit
    ip route-static 0.0.0.0 0.0.0.0 {self.input4.text()}
    user-interface vty 0 4
    authentication-mode aaa
    protocol inbound all
    protocol inbound ssh
    quit
    user-interface console 0
    authentication-mode aaa
    admin@huawei.com
    quit
    ssh server-source -i Vlanif{self.input2.text()}
    y
    ssh authorization-type default aaa
    quit
    save
    y


    """
    pyperclip.copy(commands)





def actions():
    find_com_ports()
    ready_putty()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # self.resize(300, 300)
        # self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowIcon(QIcon("C:/Users/Murad/Downloads/image1.png"))
        self.setWindowTitle("Murad")
        self.setContentsMargins(20, 20, 20, 20)

        layout = QGridLayout()
        self.setLayout(layout)

        self.label1 = QLabel("Enter Hostname")
        layout.addWidget(self.label1, 0, 0)

        self.label2 = QLabel("Vlan")
        layout.addWidget(self.label2, 1, 0)

        self.label3 = QLabel("IP Address")
        layout.addWidget(self.label3, 2, 0)

        self.label4 = QLabel("Gateway")
        layout.addWidget(self.label4, 3, 0)

        self.label5 = QLabel("Mask")
        layout.addWidget(self.label5, 4, 0)

        self.input1 = QLineEdit()
        layout.addWidget(self.input1, 0, 1)

        self.input2 = QLineEdit()
        layout.addWidget(self.input2, 1, 1)

        self.input3 = QLineEdit()
        layout.addWidget(self.input3, 2, 1)

        self.input4 = QLineEdit()
        layout.addWidget(self.input4, 3, 1)

        self.input5 = QLineEdit()
        layout.addWidget(self.input5, 4, 1)

        button = QPushButton("Submit")
        button.setFixedWidth(50)
        button.clicked.connect(lambda: config_file(self))
        button.clicked.connect(actions)
        layout.addWidget(button, 5, 1, Qt.AlignmentFlag.AlignRight)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())




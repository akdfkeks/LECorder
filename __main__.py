import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from pywinauto import *

global MARGIN_TOP
MARGIN_TOP = 20

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setUI()
        '''
        Need to create setting store file.
        '''

    def setUI(self):
        self.setWindowTitle('LECoder')
        self.center()
        self.setFixedSize(450, MARGIN_TOP + 120)
        self.setFont(QtGui.QFont("Consolas",15))

        '''Setup Buttons'''
        selectwindowBT = QPushButton("Select\nWindow", self)
        selectwindowBT.setGeometry(10,MARGIN_TOP,100,60)
        selectwindowBT.clicked.connect(self.windowSelector)

        recordBT = QPushButton("Record", self)
        recordBT.setGeometry(120,MARGIN_TOP,100,60)

        storegyopenBT = QPushButton("Open\nStoregy", self)
        storegyopenBT.setGeometry(230, MARGIN_TOP, 100, 60)

        settingsBT = QPushButton("Settings", self)
        settingsBT.setGeometry(340, MARGIN_TOP, 100,60)





    def windowSelector(self):
        QMessageBox.about(self, "Window Selector", "녹화 대상을 선택하세요")
        '''selectedWindow = '''
        self.setEnabled(False)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   app.exec_()
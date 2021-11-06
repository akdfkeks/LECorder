#-*-coding:utf-8
import sys
import os
from lib.Recoder import Recorder
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

from pywinauto import *


MARGIN_TOP = 10
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 60
selectedWindow = "Discord"
frame = 30

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
        self.setFixedSize(450, MARGIN_TOP + BUTTON_HEIGHT + 40)
        self.setFont(QtGui.QFont("Consolas",12))
        self.setButton()

    def setButton(self):
        selectwindowBT = QPushButton("Select\nWindow", self)
        selectwindowBT.setGeometry(10,MARGIN_TOP,BUTTON_WIDTH,BUTTON_HEIGHT)
        selectwindowBT.clicked.connect(self.windowSelector)

        recordBT = QPushButton("Record", self)
        recordBT.setGeometry(120,MARGIN_TOP,BUTTON_WIDTH,BUTTON_HEIGHT)
        recordBT.clicked.connect(lambda:self.recordVideo(selectedWindow, frame))

        storegyopenBT = QPushButton("Open\nStoregy", self)
        storegyopenBT.setGeometry(230, MARGIN_TOP, BUTTON_WIDTH, BUTTON_HEIGHT)
        storegyopenBT.clicked.connect(self.openStoregy)

        settingsBT = QPushButton("Settings", self)
        settingsBT.setGeometry(340, MARGIN_TOP, BUTTON_WIDTH,BUTTON_HEIGHT)

        developerinfoLabel = QLabel("GitHub Link", self)
        developerinfoLabel.setGeometry(10, MARGIN_TOP + BUTTON_HEIGHT + 10, 450,20)
        developerinfoLabel.setText('<a href="https://github.com/akdfkeks">Developer\'s GitHub</a>')
        developerinfoLabel.setOpenExternalLinks(True)




    def windowSelector(self):
        try:
            QMessageBox.about(self, "Window Selector", "녹화 대상을 선택하세요")
        except:
            QMessageBox.about(self, "Error", "Error has occured!")
        '''selectedWindow = '''
        self.setEnabled(False)
        
    def recordVideo(self, selectedWindow, frame):
        v1 = Recorder(selectedWindow, frame)
        if not (v1 == None):
            v1.record()
        
        
    def openStoregy(self):
        try:
            desktopPath = os.path.join(os.path.expanduser('~'),"Desktop","LECoder")
            if not (os.path.isdir(desktopPath)):
                os.makedirs(desktopPath)
            os.startfile(desktopPath)
        except:
            QMessageBox.about(self, "Error", "Error has occured!")

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
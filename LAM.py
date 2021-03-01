# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSlot, QTimer, pyqtSlot
# from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
import sys, io, cv2
import random, pathlib, os
from fastai.vision.all import *
from fastai.vision.widgets import *

# from google.cloud import vision
# from google.cloud.vision_v1 import types
# from PIL import ImageGrab
import pathlib

import sys,os
from fastai.vision.all import *


from GUI.scoreGUI import MyApp2
from logic.calculate import inputs_process


class MyApp1(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.className = None

    def initUI(self):
        # 시작 버튼
        btn1 = QPushButton('Start', self)
        # 버튼에 기능을 연결하는 코드
        btn1.clicked.connect(self.button1Function)

        # 사진
        pixmap = QPixmap('logo.png')
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_img.setAlignment(Qt.AlignCenter)

        # 텍스트창에 대한 라벨
        classLabel = QLabel('Class Name : ', self)
        font1 = classLabel.font()
        font1.setPointSize(20)

        # 텍스트창
        qle = QLineEdit(self)
        qle.textChanged[str].connect(self.onChanged)

        # 라벨과 텍스트창 레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(classLabel)
        hbox.addWidget(qle)

        # 레이아웃
        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(lbl_img)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # 제목 및 시작위치, 사이즈

        self.setWindowTitle('LAM')
        self.setGeometry(300, 300, 300, 200)

    # btn1이 눌리면 작동할 함수
    def button1Function(self):
        print("Start button Clicked")
        self.hide()
        createFolder('./result/' + self.className + '/chart')
        createFolder('./result/' + self.className + '/students')
        createFolder('./result/' + self.className + '/temp')
        processed_inputs = inputs_process(inputs)
        dlg = MyApp2(processed_inputs,path, self.className)
        dlg.exec_()

    # test입력창
    def onChanged(self, text):
        self.className = text


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


class person(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "'" + self.name + "'"


inputs = (
50, {person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0})

temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath

app = QApplication(sys.argv)
path = Path()
students_input = dict()
st_Obj_list = list()  # 학생 개체 모음
average_score_list = list()  # 평균 점수 기록
ex = MyApp1()
ex.show()
sys.exit(app.exec_())

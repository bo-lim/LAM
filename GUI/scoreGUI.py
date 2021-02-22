from PyQt5.QtCore import Qt, QCoreApplication, pyqtSlot, QTimer, pyqtSlot
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
import sys, io, cv2
import random, pathlib, os
from fastai.vision.all import *
from fastai.vision.widgets import *
from dataProcessing.capture import *
from GUI.resultGUI import *

from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import ImageGrab
import pathlib, os

temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath


def getInfo(dir_list, dataPath, path):
    learn_inf = load_learner(path / 'export.pkl', cpu=True)
    for item in dir_list:
        img = PILImage.create(dataPath + '/' + item)
        pred, pred_idx, probs = learn_inf.predict(img)
        name = item.split('.')[0]
        students_input[name] = pred
        print(pred)

    # 현재 데이터셋 폴더에 들어있는, 예측이 완료된 이미지 데이터들을 삭제
    # for item in dir_list:
    #     os.remove(dataPath + '/' + item)


class MyApp2(QDialog):

    def __init__(self, processed_inputs, path, className):
        super().__init__()
        print("myapp2 init 들어옴")
        self.show()
        self.inputs = processed_inputs
        self.i = 0
        self.initUI()
        self.dataPath = None
        self.dir_list = None
        self.time_class = list(range(len(class_stat)))
        self.path = path
        self.className = className

    def initUI(self):
        # 라벨 평균 
        print(self.inputs)
        self.text0 = str(round(self.inputs[0],1))
        self.label0 = QLabel(self.text0, self)
        self.label0.setAlignment(Qt.AlignCenter)  # 위치(중앙)
        font = self.label0.font()
        font.setPointSize(50)
        self.label0.setFont(font)

        # 라벨 1
        self.text1 = str(self.inputs[1][0][0]) + ' ' + str(self.inputs[1][0][1])
        self.label1 = QLabel(self.text1, self)
        self.label1.setAlignment(Qt.AlignCenter)  # 위치(중앙)
        font = self.label1.font()
        font.setPointSize(20)
        self.label1.setFont(font)

        # 라벨 2
        self.text2 = str(self.inputs[1][1][0]) + ' ' + str(self.inputs[1][1][1])
        self.label2 = QLabel(self.text2, self)
        self.label2.setAlignment(Qt.AlignCenter)  # 위치(중앙)
        font = self.label2.font()
        font.setPointSize(20)
        self.label2.setFont(font)

        # 라벨 3
        self.text3 = str(self.inputs[1][2][0]) + ' ' + str(self.inputs[1][2][1])
        self.label3 = QLabel(self.text3, self)
        self.label3.setAlignment(Qt.AlignCenter)  # 위치(중앙)
        font = self.label3.font()
        font.setPointSize(20)
        self.label3.setFont(font)

        # 라벨 4
        self.text4 = str(self.inputs[1][3][0]) + ' ' + str(self.inputs[1][3][1])
        self.label4 = QLabel(self.text4, self)
        self.label4.setAlignment(Qt.AlignCenter)  # 위치(중앙)
        font = self.label4.font()
        font.setPointSize(20)
        self.label4.setFont(font)

        # 라벨 5
        self.text5 = str(self.inputs[1][4][0]) + ' ' + str(self.inputs[1][4][1])
        self.label5 = QLabel(self.text5, self)
        self.label5.setAlignment(Qt.AlignCenter)  # 위치(중앙)
        font = self.label5.font()
        font.setPointSize(20)
        self.label5.setFont(font)

        # 종료 버튼
        quit_btn = QPushButton('Quit')  # 버튼 생성(텍스트, 버튼이 위치할 부모 위젯)
        quit_btn.resize(quit_btn.sizeHint())  # 버튼 사이즈
        quit_btn.clicked.connect(self.quit_Function)  # click시 함수 호출

        # 라벨 수직 배치
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label0)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.label5)
        self.layout.addWidget(quit_btn)
        self.setLayout(self.layout)

        # Timer 설정
        self.timer = QTimer(self)
        self.timer.start(2000)  # 10.000초마다 반복(1000=1초)
        self.timer.timeout.connect(self.timeout_run)  # 화면 갱신 함수

        # 스크린 기본 설정
        self.setWindowTitle('LAM')  # 제목
        self.setGeometry(1700, -10, 100, 2000)  # 스크린 위치와 크기
        self.show()  # 스크린 출력

    # 화면 갱신
    @pyqtSlot()
    def timeout_run(self):
        print("timeout 들어옴")
        # 캡쳐하는 부분
        capture(self.className)

        # 캡쳐된 사진을 모델에 돌리고 다시 삭제하는 부분
        dataPath = './result/' + self.className + '/students'  # dataset folder
        dir_list = os.listdir(dataPath)
        getInfo(dir_list, dataPath,self.path)

        # students_input은 {학생:예측결과} [capture의 반환결과]를 의미합니다. ex) {'kim':'a','nick', 'm', 'han':'d'}
        # student_score_update 는 students_input 결과를 보고 학생 점수표를 갱신시킵니다.
        student_score_update(students_input)

        # current_output()은 학생 점수표를 보고 (평균점수, {학생:점수})를 반환합니다.
        # inputs_process는 (평균점수, {학생:점수})를 입력받고, (평균점수, [학생, 점수] (5명 랜덤)) 형태로 변환합니다.
        # inputs를 갱신시킵니다
        self.inputs = inputs_process(current_output())

        self.text0 = str(round(self.inputs[0],1))
        self.label0.setText(self.text0)
        self.text1 = str(self.inputs[1][0][0]) + ' ' + str(self.inputs[1][0][1])
        self.label1.setText(self.text1)
        self.text2 = str(self.inputs[1][1][0]) + ' ' + str(self.inputs[1][1][1])
        self.label2.setText(self.text2)
        self.text3 = str(self.inputs[1][2][0]) + ' ' + str(self.inputs[1][2][1])
        self.label3.setText(self.text3)
        self.text4 = str(self.inputs[1][3][0]) + ' ' + str(self.inputs[1][3][1])
        self.label4.setText(self.text4)
        self.text5 = str(self.inputs[1][4][0]) + ' ' + str(self.inputs[1][4][1])
        self.label5.setText(self.text5)

    # 종료 버튼이 눌리면 작동할 함수
    def quit_Function(self):
        self.hide()
        self.timer.stop()
        print("Quit button Clicked")
        dlg = stat_app(self.className)
        # class_title = self.className
        dlg.exec_()

    def change_inputs(self, changed_inputs):
        self.inputs = changed_inputs


class_stat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
students_input = dict()

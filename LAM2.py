# -*- coding: utf-8 -*-
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

from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import ImageGrab
import pathlib, os

temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./files/zoomCapture-b179ff82aa06.json"


def getInfo(dir_list, dataPath):
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

        self.setWindowTitle('Group D Project')
        self.setGeometry(300, 300, 300, 200)

    # btn1이 눌리면 작동할 함수
    def button1Function(self):
        print("Start button Clicked")
        self.hide()
        createFolder('./' + self.className + '/students')
        createFolder('./' + self.className + '/temp')
        processed_inputs = inputs_process(inputs)
        dlg = MyApp2(processed_inputs)
        dlg.exec_()

    # test입력창
    def onChanged(self, text):
        self.className = text


def inputs_process(inputs):
    average_score = inputs[0]
    scores = inputs[1]
    students_score = list()
    for name, score in scores.items():
        students_score.append((name, score))
    random.shuffle(students_score)
    students_score = students_score[:5]
    processed_inputs = (average_score, students_score)
    return processed_inputs


class MyApp2(QDialog):

    def __init__(self, processed_inputs):
        super().__init__()
        print("myapp2 init 들어옴")
        self.show()
        self.inputs = processed_inputs
        self.i = 0
        self.initUI()
        self.dataPath = None
        self.dir_list = None
        self.time_class = list(range(len(class_stat)))

    def initUI(self):
        # 라벨 평균

        print(self.inputs)
        self.text0 = str(self.inputs[0])
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
        self.label2.setAlignment(Qt.AlignVCenter)

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
        self.setWindowTitle('My First Application')  # 제목
        self.setGeometry(1700, -10, 100, 2000)  # 스크린 위치와 크기
        self.show()  # 스크린 출력

    # 화면 갱신
    @pyqtSlot()
    def timeout_run(self):
        print("timeout 들어옴")
        # 캡쳐하는 부분
        capture(ex.className)

        # 캡쳐된 사진을 모델에 돌리고 다시 삭제하는 부분
        dataPath = './' + ex.className + '/students'  # dataset folder
        dir_list = os.listdir(dataPath)
        getInfo(dir_list, dataPath)

        # students_input은 {학생:예측결과} [capture의 반환결과]를 의미합니다. ex) {'kim':'a','nick', 'm', 'han':'d'}
        # student_score_update 는 students_input 결과를 보고 학생 점수표를 갱신시킵니다.
        student_score_update(students_input)

        # current_output()은 학생 점수표를 보고 (평균점수, {학생:점수})를 반환합니다.
        # inputs_process는 (평균점수, {학생:점수})를 입력받고, (평균점수, [학생, 점수] (5명 랜덤)) 형태로 변환합니다.
        # inputs를 갱신시킵니다
        self.inputs = inputs_process(current_output())

        self.text0 = str(self.inputs[0])
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
        dlg = stat_app()
        class_title = ex.className
        dlg.exec_()

    def change_inputs(self, changed_inputs):
        self.inputs = changed_inputs


class student:
    def __init__(self, name=""):
        self.name = name  # 이름
        self.score = 60  # 현재 점수
        self.reaction = 0  # 리액션 횟수
        self.score_list = list()  # 점수 기록

    # 1분당 1점씩 점수 감소
    def auto_minus(self):
        self.score -= 1

    # 리액션할 경우 점수 증가
    def React(self):
        self.score += 5
        if self.score > 100:
            self.score = 100
        self.reaction += 1  # 리액션 횟수 증가
        self.score_list.append(self.score)  # 점수 변화기록

    # 아무것도 안할 경우 점수만 기록
    def Nope(self):
        self.score_list.append(self.score)  # 점수 변화기록

    # 프레임에 없을 경우 점수 감소
    def OutofFrame(self):
        self.score -= 5
        if self.score < 0:
            self.score = 0
        self.score_list.append(self.score)  # 점수 변화기록


# Main function: 입력값을 학생 객체에 갱신시킨다.
def student_score_update(students_input):
    for name, result in students_input.items():
        student_in = False  # 매칭되는 학생 존재 여부
        # 만약 매칭되는 학생 개체가 있으면 갱신한다.
        for st in st_Obj_list:
            if name == st.name:
                student_in = True
                if result == 'clap' or result == 'nod' or result == 'smile':
                    st.React()
                elif result == 'default':
                    st.Nope()
                elif result == 'yawn' or result == 'outOfFrame':
                    st.OutofFrame()

        # 매칭되는 학생 개체가 없으면 생성한다.
        if student_in == False:
            st_Obj = student(name)
            st_Obj_list.append(st_Obj)
            if result == 'smile' or result == 'nod' or result == 'clap':
                st_Obj.React()
            elif result == 'default':
                st_Obj.Nope()
            elif result == 'outOfFrame' or result == 'yawn':
                st_Obj.OutofFrame()


def current_output():
    total_score = 0
    # 현재 수업 평균 점수 계산 및 기록 및 출력
    average_score = 60
    for st in st_Obj_list:
        total_score += st.score
    average_score = total_score / len(st_Obj_list)
    # 수업 평균 점수를 기록한다
    average_score_list.append(average_score)

    # student_output: {학생: 현재 점수, 학생: 현재 점수, 학생: 현재 점수}
    student_output = dict()
    for st in st_Obj_list:
        student_output[st.name] = st.score
    # 최종 out: (수업평균점수, student_output)
    return (average_score, student_output)


def final_output():
    # final_student_output: {학생: 평균 점수, 학생: 평균 점수, 학생: 평균점수}
    final_student_output = dict()
    for st in st_Obj_list:
        final_student_score = sum(st.score_list) / len(st.score_list)
        final_student_output[st.name] = (final_student_score, st.reaction)
    # 수업 전체 평균 점수
    final_class_score = sum(average_score_list) / len(average_score_list)
    # 최종 out: (final_student_output, 전체 최종 수업 평균, 수업 평균 점수 배열)
    return (final_student_output, final_class_score, average_score_list)


class stat_app(QDialog):

    def __init__(self):
        super().__init__()
        self.setVisible(True)
        self.student_stat = None
        self.class_stat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.time_class = None
        self.initUI()

    def initUI(self):
        print("stat_app initUI로 들어옴")
        grid = QGridLayout()
        self.setLayout(grid)

        x, y, z = final_output()
        self.get_info(x, y, z)

        # Graph drawing
        self.fig = plt.Figure()
        ax = self.fig.add_subplot(111)
        ax.set_title(ex.className + "\n" + now + "\n" + "Class Attention Guage")
        ax.set_xlabel('Time(divided by 10)')
        ax.set_ylabel('Guage')
        self.time_class = list(range(len(self.class_stat)))
        ax.plot(self.time_class, self.class_stat, label='Class Attention Guage')
        self.canvas = FigureCanvas(self.fig)

        # Student stat printing
        self.stat_tb = QTableWidget(self)
        self.stat_tb.setRowCount(len(self.student_stat))
        self.stat_tb.setColumnCount(3)
        self.set_stat_table()

        # Layout
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)
        grid.addWidget(QLabel('Final Stat'), 0, 0)
        grid.addLayout(leftLayout, 1, 0)
        grid.addWidget(QLabel('Student Stat'), 0, 1)
        grid.addWidget(self.stat_tb, 1, 1)

        # Add export button
        btn = QPushButton('Export', self)
        grid.addWidget(btn, 2, 1)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.export_clicked)

        self.setWindowTitle('Final Result Data')
        self.setWindowIcon(QIcon("Pictures/LAM로고.png"))
        self.setGeometry(500, 400, 1015, 700)
        self.show()

        # setting up student table

    def set_stat_table(self):
        column_headers = ['name', 'score', 'reaction']
        row = 0
        print("set_stat_table 정보")
        print(self.student_stat)
        self.stat_tb.setHorizontalHeaderLabels(column_headers)
        for key, value in self.student_stat.items():
            self.stat_tb.setItem(row, 0, QTableWidgetItem(key))
            self.stat_tb.setItem(row, 1, QTableWidgetItem(str(value[0])))
            self.stat_tb.setItem(row, 2, QTableWidgetItem(str(value[1])))
            row += 1

        # if export button is clicked,
        # student stat .csv // class graph .jpg
        # are exported

    def get_info(self, st_stat, class_score, c_stat):
        print("get_info 정보")
        print(st_stat)
        print(class_score)
        print(c_stat)
        self.student_stat = st_stat
        self.class_stat = c_stat
        print("self 정보")
        print(self.student_stat)
        print(self.class_stat)

    def export_clicked(self):
        print("Export 버튼의 정보")
        print(self.class_stat)
        print(self.student_stat)
        f = open(ex.className + '_csv' + now + '_result.csv', 'w', encoding="UTF-8")
        f.write('time' + ',' + 'avg' + '\n')
        row = 0
        for value, row in zip(self.class_stat, range(len(self.class_stat))):
            f.write(str(row) + ',' + str(value) + '\n')
        f.write('\n')

        f.write('name' + ',' + 'score' + ',' + 'reaction' + '\n')
        for key, value in self.student_stat.items():
            f.write(key + ',' + str(value[0]) + ',' + str(value[1]) + '\n')
        f.close()
        self.fig.savefig(ex.className + '_jpg' + now + '_graph.jpg')


class person(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "'" + self.name + "'"


def capture(classDir):
    img_full = ImageGrab.grab()
    width, height = img_full.size
    tempDir = classDir + '/temp/temp.png'
    img_full.crop((width / 18, height / 7, width * (14 / 18), height * (6 / 7))).save(tempDir, "PNG")
    faceCrop(tempDir, classDir)


def faceCrop(tempDir, classDir):
    # print("tempDir :"+tempDir)
    # print("classDir :"+classDir)

    tempImg = cv2.imread(tempDir)
    height, width, channel = tempImg.shape

    with io.open(tempDir, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(image=image)
    texts = response.text_annotations

    print(len(texts))
    if len(texts) > 2 and len(texts) < 50:
        firstVertices = texts[1].bounding_poly.vertices
        f_cornerX = firstVertices[3].x
        secondVertices = texts[2].bounding_poly.vertices
        s_cornerX = secondVertices[3].x

        dx = s_cornerX - (f_cornerX + firstVertices[2].x)
        dy = int(dx * 0.6)

        if not os.path.isdir(classDir + "/students"):
            os.mkdir(classDir + "/students")
            print(classDir + "/students" + "폴더 만들어짐")
        print("if문 안걸림")
        # print(texts[1:])
        # COUNT = 0
        for text in texts[1:]:
            print("facecrop for문 안으로 들어옴")
            # cv2.rectangle(img=tempImg, pt1=(text.bounding_poly.vertices[0].x,text.bounding_poly.vertices[0].y), pt2=(text.bounding_poly.vertices[2].x,text.bounding_poly.vertices[2].y),color=(255,0,0))
            print(text.description)
            print("In")
            path = classDir + "/students/"
            vertex = text.bounding_poly.vertices[3]
            leftTopY = vertex.y - dy - 5
            rightBotX = vertex.x + dx + 5
            if leftTopY < 0:
                leftTopY = 0
            if rightBotX > width:
                rightBotX = width
            face = tempImg[leftTopY: vertex.y, vertex.x: rightBotX]
            if rightBotX - vertex.x > width / 7 and vertex.y - leftTopY > height / 7:
                print(text.description)
                # print(leftTopY, vertex.y, vertex.x, rightBotX)
                cv2.imwrite(path + text.description + '.png', face)
                print(text.description + "작성 중..")
                # cv2.putText(tempImg, str(COUNT), (leftTopY, vertex.x), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0))
                # cv2.rectangle(img=tempImg, pt1=(vertex.x, (leftTopY)), pt2=((rightBotX), vertex.y), color=(0, 255, 0))
                # COUNT += 1
            else:
                print("HI!")

        # cv2.imshow("img", tempImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        print("Error: too many")


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


className = ''
inputs = (
50, {person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0, person(" "): 0})
status = False
student_stat = {' ': (0, 0), ' ': (0, 0), ' ': (0, 0), ' ': (0, 0)}
class_stat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
now = datetime.now().strftime('%Y-%m-%d_%H%M')

app = QApplication(sys.argv)
path = Path()
students_input = dict()
st_Obj_list = list()  # 학생 개체 모음
average_score_list = list()  # 평균 점수 기록
ex = MyApp1()
ex.show()
sys.exit(app.exec_())

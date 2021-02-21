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


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./dataProcessing/files/zoomCapture-b179ff82aa06.json"


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
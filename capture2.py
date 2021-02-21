### NOTICE
### pip install --upgrade google-cloud-vision 해야해요
### files 폴더 안에 있는 파일 때문에 private repository로 둘게요
### GUI 쪽에서 합쳐주시면 될 부분은 파일 가장 하단에 있습니다


import io
import os
import cv2
import time

from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import ImageGrab
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "./files/zoomCapture-b179ff82aa06.json"



##### ZOOM CAPTURE

def capture(classDir):
    img_full = ImageGrab.grab()
    width, height = img_full.size
    tempDir = classDir+'/temp/temp.png'
    img_full.crop((width / 18, height / 7, width * (14 / 18), height * (6 / 7))).save(tempDir,"PNG")
    faceCrop(tempDir,classDir)

def faceCrop(tempDir,classDir):

    tempImg = cv2.imread(tempDir)
    height, width,channel = tempImg.shape

    with io.open(tempDir,'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if len(texts)>2 and len(texts)<50:
        firstVertices = texts[1].bounding_poly.vertices
        f_cornerX = firstVertices[3].x
        secondVertices = texts[2].bounding_poly.vertices
        s_cornerX = secondVertices[3].x

        dx = s_cornerX - (f_cornerX + firstVertices[2].x)
        dy = int(dx*0.6)

        if not os.path.isdir(classDir+"/students"):
            os.mkdir(classDir+"/students")

        for text in texts[1:]:
            path = classDir+"/students/"
            vertex = text.bounding_poly.vertices[3]
            leftTopY = vertex.y -dy -5
            rightBotX = vertex.x + dx + 5
            if leftTopY<0:
                leftTopY = 0
            if rightBotX>width:
                rightBotX = width
            face = tempImg[leftTopY : vertex.y, vertex.x : rightBotX]
            if rightBotX - vertex.x > width/7 and vertex.y-leftTopY > height/7:
                print(leftTopY, vertex.y, vertex.x, rightBotX)
                cv2.imwrite(path+text.description+'.png',face)
                # cv2.rectangle(img=tempImg, pt1=(vertex.x, (leftTopY)),pt2=((rightBotX), vertex.y),color=(0, 255, 0))

        # cv2.imshow("img",tempImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        print("Error: too many")



##### GUI

on = False
count = 0

# if startbuttonclicked:
#    on = True

className = input("ClassName: ") # 이 부분에 입력받은 수업명 넣어줘야함
if not os.path.isdir("./"+className):
    os.mkdir("./"+className)
if not os.path.isdir("./"+className+"/temp"):
    os.mkdir("./"+className+"/temp")
classDir = "./"+className

# while True:
#   if endbuttonclicked:
#       on = False
#       break
#   if on:
capture(classDir) # 이 capture 함수가 반복 실행돼야함. while문 구현되면 if on 에 해당하게 들여쓰기 해주세요
#     time.sleep(10) # 10초마다 실행하게끔 조절
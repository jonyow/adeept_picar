
import cvlib
from cvlib.object_detection import draw_bbox
import cv2
import random

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

useTiny=False
useGPU=False
yoloConfidence=0.3




def runFaceClassifer(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_img,
                                    scaleFactor=1.10,  #each iteraction recscales search down by 5%. Larger number less accurate
                                    minNeighbors=10)  # how many neighbours to search around.

    border_thickness = 3
    border_colour = (255,0,0)

    #print( "No. of faces: " + len(faces).__str__() )

    for x, y, w, h in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), border_colour, border_thickness)

    #img_width = 1000
    #re_img = cv2.resize(img, (img_width, int(img.shape[0]/ img.shape[1] * img_width)) )

    return img, len(faces)

def runObjectClassifier(img):
    global cvCache

    if useTiny:
        model = 'yolov3-tiny'
    else:
        model = ''

    # only run detection on 1 in X frames for performance
   # if random.randint(1, 3) == 1 or cvCache is None:
    cvCache = cvlib.detect_common_objects(img,
                                        model=model,
                                        enable_gpu=useGPU,
                                        confidence=yoloConfidence)

    bbox, label, conf = cvCache
    img = draw_bbox(img, bbox, label, conf, write_conf=True)

    return img, len(label)

def init():
    img = cv2.imread("./logo.png")
    out = cvlib.detect_common_objects(img, enable_gpu=useGPU, confidence=yoloConfidence)

init()
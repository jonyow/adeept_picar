import cv2
import numpy as np
import os
import pickle

import datetime


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./custom_haar_files/trainer.yml')

cascadePath = "./custom_haar_files/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# Define min window size to be recognized as a face
minW = 0.1 * 640
minH = 0.1 * 480

ID_NAME_PICKLE = './custom_haar_files/id_name_dict.pkl'
if not os.path.exists(ID_NAME_PICKLE):
    id_name_dict={}
else:
    id_name_dict = pickle.load(open(ID_NAME_PICKLE, 'rb'))

lastSound = datetime.datetime.now()

def run_detector(img, play_sound = False, sound_min_gap_secs = 10):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # If confidence is less them 100 ==> "0" : perfect match
        if confidence > 1:
            name = id_name_dict.get(str(id))
            confidence = "  {0}%".format(round(100 - confidence))

            if play_sound:
                pass


                # import create_custom_sounds
                # global lastSound
                # if (datetime.datetime.now() - lastSound).seconds > sound_min_gap_secs:
                #     if create_custom_sounds.play_person_spotted(name):
                #         lastSound = datetime.datetime.now()

        else:
            name = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(
            img,
            str(name),
            (x + 5, y - 5),
            font,
            1,
            (255, 255, 255),
            2
        )
        cv2.putText(
            img,
            str(confidence),
            (x + 5, y + h - 5),
            font,
            1,
            (255, 255, 0),
            1
        )

    return img


def test_detector():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()

        img = run_detector(img)

        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

    return
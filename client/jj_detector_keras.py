

import os
import sys

src_path = os.path.join(os.getcwd(), "jjdetector")
sys.path.append(src_path)

from jjdetector.keras_yolo3.yolo import YOLO

from PIL import Image
import cv2
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# Set up folder names for default values

model_weights = os.path.join(src_path, "trained_weights_final_jy_v2.h5")
model_classes = os.path.join(src_path, "data_classes.txt")
anchors_path = os.path.join(src_path, "keras_yolo3", "model_data", "yolo_anchors.txt")

FLAGS = None

min_confidence = 0.6

# define YOLO detector
yolo = YOLO(
    **{
        "model_path": model_weights,
        "anchors_path": anchors_path,
        "classes_path": model_classes,
        "score": min_confidence,
        "gpu_num": 1,
        "model_image_size": (416, 416
                             ),
    }
)

# labels to draw on images
class_file = open(model_classes, "r")
input_labels = [line.rstrip("\n") for line in class_file.readlines()]
print("Found {} input labels: {} ...".format(len(input_labels), input_labels))

#test =  Image.open(r"C:\Users\jon_y\Documents\PythonProjects\CustomYolov3Detector\images\resized\IMG_0718.jpg")

def runYoloDetector(pil_img):

    prediction, image_out = yolo.detect_image(pil_img)

    return prediction, image_out


def runJJDetector(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #print('Running JJ...')
    pil_img = Image.fromarray(img)
    predictions, pil_img_out = yolo.detect_image(pil_img, show_stats=False)
    #print(predictions)
    cv_img = cv2.cvtColor(np.array(pil_img_out), cv2.COLOR_RGB2BGR)
    return cv_img

def runVideo():

    video = cv2.VideoCapture(0)

    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # video.set(cv2.CAP_PROP_FRAME_HEIGHT, 10)

    timestamps = []
    num_faces_list = []


    while True:
        check, img = video.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)

        # face_frame, num_objs = runFaceClassifer(frame)
        #output_frame, num_objs = runObjectClassifier(frame)

        predictions, pil_img_out = yolo.detect_image(pil_img)

        cv_img = cv2.cvtColor(np.array(pil_img_out), cv2.COLOR_RGB2BGR)

        # num_faces_list.append(num_objs)

        # plt.clf()
        # plt.bar(timestamps, num_faces_list, 0.1, color='blue')
        # fig.canvas.draw()

        cv2.imshow("Test", cv_img)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
    # Close the current yolo session
    #yolo.close_session()

# import pickle
#
# img = pickle.load(open('source2.p', 'rb'))
#
# pil_img = Image.fromarray(img)
#
# predictions, pil_img_out = yolo.detect_image(pil_img)
#
# cv_img = cv2.cvtColor(np.array(pil_img_out), cv2.COLOR_RGB2BGR)
#
# # num_faces_list.append(num_objs)
#
# # plt.clf()
# # plt.bar(timestamps, num_faces_list, 0.1, color='blue')
# # fig.canvas.draw()
#
# cv2.imshow("Test", cv_img)
#
# key = cv2.waitKey(1)
#
#
# cv2.destroyAllWindows()


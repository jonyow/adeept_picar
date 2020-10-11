

import jj_detector_keras
import pickle
import cv2

test_img = pickle.load(open('source.p', 'rb'))

img_out = jj_detector_keras.runJJDetector(test_img)

cv2.imshow("Test", img_out)

cv2.waitKey(1)

cv2.destroyAllWindows()
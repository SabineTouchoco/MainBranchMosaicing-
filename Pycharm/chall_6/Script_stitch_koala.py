import cv2
import os
#dir_ = os.path.dirname(__file__)
#filename0 = os.path.join(dir_, "ressources/koala_0.png")
#filename1 = os.path.join(dir_, "ressources/koala_1.png")

stitcher = cv2.createStitcher(False)
img0 = cv2.imread("ressources/koala_0.png")
img1 = cv2.imread("ressources/koala_1.png")
result = stitcher.stitch((img0, img1))

cv2.imwrite("ressources/koala_result.png", result[1])
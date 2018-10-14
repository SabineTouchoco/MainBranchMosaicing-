import cv2
import os
#dir_ = os.path.dirname(__file__)
#filename0 = os.path.join(dir_, "ressources/koala_0.png")
#filename1 = os.path.join(dir_, "ressources/koala_1.png")

stitcher = cv2.createStitcher(False)
img0 = cv2.imread("Inputs/0.jpg")
img1 = cv2.imread("Inputs/1.jpg")
img2 = cv2.imread("Inputs/2.jpg")
result = stitcher.stitch((img0, img1, img2))

cv2.imwrite("Outputs/result.jpg", result[1])
import cv2
import os
import numpy as np

stitcher = cv2.createStitcher(False)
img0 = cv2.imread("Outputs//frame0.jpg")
img1 = cv2.imread("Outputs//frame1.jpg")
img2 = cv2.imread("Outputs//frame2.jpg")
img3 = cv2.imread("Outputs//frame3.jpg")
img4 = cv2.imread("Outputs//frame4.jpg")
img5 = cv2.imread("Outputs//frame5.jpg")
img6 = cv2.imread("Outputs//frame6.jpg")
img7 = cv2.imread("Outputs//frame7.jpg")
img8 = cv2.imread("Outputs//frame8.jpg")
img9 = cv2.imread("Outputs//frame9.jpg")
img10 = cv2.imread("Outputs//frame10.jpg")
result = stitcher.stitch((img1, img2, img3, img4, img5))
cv2.imwrite("Outputs//Mosaique.jpg", result[1])
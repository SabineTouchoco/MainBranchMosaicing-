import cv2
import numpy as np
from matplotlib import pyplot as plt

img0 = cv2.imread("inputs/img_5.png")
img1 = cv2.imread("inputs/img_6.png")

# ORB : finding keypoints and descriptors in the pictures
orb = cv2.ORB_create()

kp0 = orb.detect(img0, None)
kp1 = orb.detect(img1, None)

kp0, des0 = orb.compute(img0, kp0)
kp1, des1 = orb.compute(img1, kp1)

# draw only keypoints location,not size and orientation
res0 = cv2.drawKeypoints(img0, kp0, None, color=(0, 255, 0), flags=0)
plt.imshow(img0), plt.show()
res1 = cv2.drawKeypoints(img1, kp1, None, color=(255, 0, 0), flags=0)
plt.imshow(img1), plt.show()

#FLANN

#RANSAC


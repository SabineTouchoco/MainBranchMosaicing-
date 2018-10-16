# import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('Inputs/ResultAligned015.jpg',0)
imgR = cv2.imread('Inputs/frame1.jpg',0)

# stereo = cv2.createStereoBM(numDisparities=16, blockSize=15)
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL, imgR)  # Permet de recup la profondeur des objets dans image mais que faire de cela
plt.imshow(disparity, 'gray')
plt.show()

# cv2.imwrite("Outputs/Result.jpg", disparity)


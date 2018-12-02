####################################################################################################
# File name: dense_optical_flow.py
# Created by: Julian Paul
# Date created: 11/16/2018
# Date last modified: 11/16/2018
# Source: https://docs.opencv.org/3.4/d7/d8b/tutorial_py_lucas_kanade.html
# Description: It computes the optical flow for all the points in the frame and displays the result.
####################################################################################################

import cv2
import numpy as np


cap = cv2.VideoCapture("input/t4_avi.avi")

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

while 1:
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow('frame2', rgb)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('output/opticalfb.png', frame2)
        cv2.imwrite('output/opticalhsv.png', rgb)
    prvs = next

cap.release()
cv2.destroyAllWindows()

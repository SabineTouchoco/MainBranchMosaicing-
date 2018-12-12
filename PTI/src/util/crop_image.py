####################################################################################################
# File name: crop_image.py
# Created by: Julian Paul
# Date created: 12/05/2018
# Date last modified: 12/05/2018
# Description: Crops an image given its corner bounds.
####################################################################################################

import cv2

startX = 100
endX = 600
startY = 100
endY = 600

count = 10

for i in range(1, count):
    img = cv2.imread("output/frame-%d.jpg" % count)
    crop_img = img[startX:endX, startY:endY]
    cv2.imwrite("output/cropped_frame-%d.jpg" % count, crop_img)

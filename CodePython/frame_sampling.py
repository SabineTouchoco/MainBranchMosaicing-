import cv2
import numpy as np

filename = "inputs/T4.avi"

video = cv2.VideoCapture(filename)
fps = video.get(cv2.CAP_PROP_FPS)
print('Video fps : ', fps)

frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
print('Video frame count : ', frame_count)

count = 0
for i in range(int(frame_count)):
    success, img = video.read()
    if success and (i % (int(fps/3))) == 0:
        img_path = "outputs/img_" + str(count) + ".png"
        cv2.imwrite(img_path, img)
        count += 1
        print("img " + str(i) + " sampled.")

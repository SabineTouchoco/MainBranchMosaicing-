import cv2
import numpy as np

filename = "inputs/T4.avi"

video = cv2.VideoCapture(filename)
fps = video.get(cv2.CAP_PROP_FPS)
print('Video fps : ', fps)

width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
print('Video width : ', width)

frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
print('Video frame count : ', frame_count)

count = 0
delta = 20
center = int(width/2)
offset = 0
for i in range(int(frame_count)):
    success, img = video.read()
    if success:
        line = img[:, (center - delta + offset):(center + delta + offset), :]
        if count > 0:
            result = np.concatenate((result, line), 1)
        else:
            result = line
        #img_path = "outputs/img_" + str(count) + ".png"
        #cv2.imwrite(img_path, img)
        count += 1
        print("img " + str(i) + " sampled.")
print("Done.")

img_path = "outputs/result.png"
cv2.imwrite(img_path, result)

print("Image saved.")
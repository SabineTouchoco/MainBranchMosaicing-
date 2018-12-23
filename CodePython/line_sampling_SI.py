import cv2
import numpy as np

filename = "inputs/T4_HFV_Charpennes - Charles Hernu.mp4"

video = cv2.VideoCapture(filename)
fps = video.get(cv2.CAP_PROP_FPS)
print('Video fps : ', fps)

width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
print('Video width : ', width)

frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
print('Video frame count : ', frame_count)

count = 0
delta = 25
center = int(width/2)
offset = 0

for i in range(int(frame_count)):
    #delta = int(190*(count/frame_count)*(count/frame_count)-388*(count/frame_count)+209)
    success, img = video.read()
    if success:
        line = img[:, (center - delta + offset):(center + delta + offset), :]
        if count > 0:
            result = np.concatenate((line, result), 1)
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
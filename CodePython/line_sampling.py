import cv2
import numpy as np

filename = "inputs/T4_HFV_Manufacture-Montluc.mp4"

video = cv2.VideoCapture(filename)
fps = video.get(cv2.CAP_PROP_FPS)
print('Video fps : ' + str(fps))

width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
print('Video width : ' + str(width))

frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
print('Video frame count : ' + str(frame_count))

count = 0
center = int(width/2)
offset = 0
for i in range(int(frame_count)):
    success, img = video.read()
    if success :
        # delta = int(50/((count/100)+1))
        delta_0 = 80
        delta = delta_0 - i * delta_0 / frame_count
        delta = int(delta)
        line = img[:, (center - delta + offset):(center + delta + offset), :]
        if count > 0:
            result = np.concatenate((line, result), 1)
        else:
            result = line
        # img_path = "outputs/img_" + str(count) + ".png"
        # cv2.imwrite(img_path, img)
        count += 1
        print("img " + str(i) + " sampled.")
print("Done.")

img_path = "outputs/result_delta_var.png"
cv2.imwrite(img_path, result)

print("Image saved.")
import cv2
import numpy as np

# Fonction permettant de tourner une image
def rotate_image(mat, angle):

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

filename = "D://sabin//Documents//Etudes//INSA 3//Challenge//Partage//CodePython//Inputs//QuaiADroite//Tram//P1190072.MOV"

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
    img = rotate_image(img, -90)
    if success :
        # delta = int(50/((count/100)+1))
        delta_0 = 80
        delta = delta_0 - i * delta_0 / (frame_count*1.33)
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

img_path = "Outputs/LineSampling60fps.jpg"
cv2.imwrite(img_path, result)

print("Image saved.")
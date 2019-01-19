import cv2
import numpy as np
from matplotlib import pyplot as plt

def augmente_moi(a, b):
    return 30 + a + b

filename = "Inputs//T4_HFV_CharpennesCharlesHernu.mp4"

video = cv2.VideoCapture(filename)

width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
print('Video width : ' + str(width))

height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('Video height : ' + str(height))

center = int(width/2)
offset = 0

hauteur_max = height - 100 # Ronge la partie du bas de l'image quand hauteur max augmente.
hauteur_min = 100 # Ronge la partie du haut de l'image quand hauteur min augmente.

success, img = video.read()
img = img[int(hauteur_min):int(hauteur_max),:,:]
result = img[:, center:int(width-1), :]



img_path = "Outputs/result_delta_var.png"
cv2.imwrite(img_path, result)

print("Image saved.")
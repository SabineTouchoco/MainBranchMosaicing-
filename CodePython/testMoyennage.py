import cv2
import numpy as np
from matplotlib import pyplot as plt

img_path = "Outputs/result.png"
img = cv2.imread(img_path, 1)

result = cv2.blur(img,(10,10))
img_path = "Outputs/filtered_result.png"
cv2.imwrite(img_path, result)

print("Image saved.")
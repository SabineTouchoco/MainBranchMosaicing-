import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('Inputs//ToFindWithTempMatching.png',0)
img2 = img.copy()
template = cv.imread('Inputs//WhereToFindWithTempMatching.png',0)
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()

    # k = cv2.waitKey(100) & 0xff

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
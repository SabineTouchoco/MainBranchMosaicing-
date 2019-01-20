import numpy as np
import cv2

filename = "Inputs//videoplayback.mp4"
filename = "Inputs//QuaiADroite//Tram//P1190082.MOV"

video = cv2.VideoCapture(filename)
fgbg = cv2.createBackgroundSubtractorMOG2()

frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
print('Video frame count : ' + str(frame_count))

count = 0

for i in range(int(frame_count)):
    success, img = video.read()

    # Parametrage masque
    # None = cv.BackgroundSubtractorMOG2.setBackgroundRatio(ratio) # Sets the "background ratio" parameter of the algorithm.
    # None = cv.BackgroundSubtractorMOG2.setComplexityReductionThreshold(ct) # Sets the complexity reduction threshold.
    # None = cv.BackgroundSubtractorMOG2.setDetectShadows(detectShadows) # Enables or disables shadow detection.
    # None = cv.BackgroundSubtractorMOG2.setHistory(history) # Sets the number of last frames that affect the background model.
    # None = cv.BackgroundSubtractorMOG2.setNMixtures(nmixtures) # Sets the number of gaussian components in the background model. The model needs to be reinitalized to reserve memory.
    # None = cv.BackgroundSubtractorMOG2.setShadowThreshold(threshold) # Sets the shadow threshold.
    # None = cv.BackgroundSubtractorMOG2.setShadowValue(value) # Sets the shadow value.
    # None = cv.BackgroundSubtractorMOG2.setVarInit(varInit) # Sets the initial variance of each gaussian component.
    # None = cv.BackgroundSubtractorMOG2.setVarMax(varMax)
    # None = cv.BackgroundSubtractorMOG2.setVarMin(varMin)
    # None = cv.BackgroundSubtractorMOG2.setVarThreshold(varThreshold) # Sets the variance threshold for the pixel-model match.
    # None = cv.BackgroundSubtractorMOG2.setVarThresholdGen(varThresholdGen) # Sets the variance threshold for the pixel-model match used for new mixture component generation.

    fgbg.setBackgroundRatio(0.9) # Sets the "background ratio" parameter of the algorithm.
    fgbg.setComplexityReductionThreshold(0) # Sets the complexity reduction threshold.
    fgbg.setDetectShadows(0) # Enables or disables shadow detection.
    fgbg.setHistory(10) # Sets the number of last frames that affect the background model.
    # fgbg.setNMixtures(10) # Sets the number of gaussian components in the background model. The model needs to be reinitalized to reserve memory.
    # fgbg.setShadowThreshold(255) # Sets the shadow threshold.
    # fgbg.setShadowValue(0) # Sets the shadow value.
    # fgbg.setVarInit(2) # Sets the initial variance of each gaussian component.
    # fgbg.setVarMax(255)
    # fgbg.setVarMin(125)
    # fgbg.setVarThreshold(120) # Sets the variance threshold for the pixel-model match.
    # None = cv.BackgroundSubtractorMOG2.setVarThresholdGen(varThresholdGen) # Sets the variance threshold for the pixel-model match used for new mixture component generation.

    if success:
        fgmask = fgbg.apply(img)
        mask = fgmask
        res = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow('original', img)
        cv2.imshow('frame', res)
        # cv2.imshow('frame', fgmask)
        k = cv2.waitKey(100) & 0xff

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # img_path = "Outputs/img_" + str(count) + ".png"
        # cv2.imwrite(img_path, res)
        count += 1
print("Done.")

video.release()
cv2.destroyAllWindows()
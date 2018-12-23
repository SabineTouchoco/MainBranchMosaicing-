# coding: latin-1
import cv2
import sys
import numpy as np

def extract_image_one_fps(video_source_path):

    vidcap = cv2.VideoCapture(video_source_path)

    video_capture = cv2.VideoCapture()
    if not video_capture.open(video_source_path):
        print >> sys.stderr, 'Error: Cannot open video file ' + video_source_path
        return

    count = 0
    success = True

    vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO,1) # Relative position of the video file: 0 - start of the film, 1 - end of the film.
    video_nb_ms = vidcap.get(cv2.CAP_PROP_POS_MSEC)  # Current position of the video file in milliseconds.
    nb_ms = 33 # Echantillonage video toutes les nb_ms
    print(video_nb_ms)
    print(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    while success and (count*nb_ms) < video_nb_ms:

        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * nb_ms))  # Current position of the video file in milliseconds.
        success, image = vidcap.read()

        ## Stop when last frame is identified
        image_last = cv2.imread("frame{}.png".format(count - 1))
        if np.array_equal(image, image_last):
            break

        cv2.imwrite("Outputs//frame%d.jpg" % count, image)  # save frame as PNG file
        count += 1

video_source_path = "Inputs//T4_HFV_ArchivesDepartementales.mp4"
extract_image_one_fps(video_source_path)
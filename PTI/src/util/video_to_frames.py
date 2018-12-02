####################################################################################################
# File name: video_to_frames.py
# Created by: Challenge group
# Date created: 11/01/2018
# Date last modified: 11/01/2018
# Description: Convert a video into a set of frames in the output folder given the sampling time in
# ms.
####################################################################################################

import sys

import cv2
import numpy as np


def extract_image_one_fps(source_path):
    video = cv2.VideoCapture(source_path)

    video_capture = cv2.VideoCapture()
    if not video_capture.open(source_path):
        print >> sys.stderr, 'Error: Cannot open video file ' + source_path
        return

    count = 0
    success = True

    # Relative position of the video file: 0 - start of the film, 1 - end of the film.
    video.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)

    # Current position of the video file in milliseconds.
    video_size_ms = video.get(cv2.CAP_PROP_POS_MSEC)

    # Sampling in ms
    sampling = 300
    print(video_size_ms)

    while success and (count * sampling) < video_size_ms:
        # Current position of the video file in milliseconds.
        video.set(cv2.CAP_PROP_POS_MSEC, (count * sampling))
        success, image = video.read()

        # Stop when last frame is identified
        image_last = cv2.imread("frame{}.png".format(count - 1))
        if np.array_equal(image, image_last):
            break

        cv2.imwrite("output/frame-%d.jpg" % count, image)  # save frame as PNG file
        count += 1


video_source_path = "input/m6_test.mp4"
extract_image_one_fps(video_source_path)

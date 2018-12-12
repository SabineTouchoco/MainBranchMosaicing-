####################################################################################################
# File name: video_to_frames.py
# Created by: Challenge group
# Date created: 11/01/2018
# Date last modified: 11/01/2018
# Description: Convert a video into a set of frames in the output folder given the sampling time in
# ms, then process these frames to provide the Darknet network the right input in terms of size,
# resolution and ROI.
####################################################################################################

import sys

import cv2
import imutils
import numpy as np

####################################################################################################
# Video to preprocess
video_source_path = "input/13-mermoz1.mp4"

# Cropping attributes
margin_start = 100
margin_end = 0
margin_bottom = 350
margin_top = 500
####################################################################################################


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
    sampling = 500
    print(video_size_ms)

    while success and (count * sampling) < video_size_ms:
        # Current position of the video file in milliseconds.
        video.set(cv2.CAP_PROP_POS_MSEC, (count * sampling))
        success, image = video.read()

        # Stop when last frame is identified
        image_last = cv2.imread("frame{}.png".format(count - 1))
        if np.array_equal(image, image_last):
            break
        width = image.shape[0]
        height = image.shape[1]

        # Crop the image
        image = image[margin_end:(width - margin_start), margin_top:(height - margin_bottom)]

        # Rotate the image
        image = imutils.rotate_bound(image, 90)

        # Save frame as PNG file
        cv2.imwrite("output/frame-%d.jpg" % count, image)
        count += 1


extract_image_one_fps(video_source_path)

from __future__ import print_function
import cv2
import numpy as np
import sys

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.8

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

def GetDeplacement(im1, im2):
    # Convert images to gray scale
    im1gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    kp1, descriptors1 = orb.detectAndCompute(im1gray, None)
    kp2, descriptors2 = orb.detectAndCompute(im2gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    #imMatches = cv2.drawMatches(im1, kp1, im2, kp2, matches, None)
    #cv2.imwrite("Outputs/ResultMatches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    pointsDeplacements = np.zeros((len(matches), 2), dtype=np.float32)

    # Get value of deplacement/move
    averageMove = 0
    minMove = 6000
    maxMove = 0
    itMove = 0

    for i, match in enumerate(matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt
        pointsDeplacements[i, :] = points1[i, :] - points2[i, :]
        # print('Point 1 : ', points1[i, :])
        # print('Point 2 : ', points2[i, :])
        # print('Difference : ', pointsDeplacements[i, :])
        # print('delta x : ', pointsDeplacements[i, 0])
        # print('delta y : ', pointsDeplacements[i, 1])

        if abs(pointsDeplacements[i, 1]) < 2:   # if delta y is not abberant
            # print('Difference : ', pointsDeplacements[i, :])
            # print('delta x : ', pointsDeplacements[i, 0])
            # print('delta y : ', pointsDeplacements[i, 1])
            if pointsDeplacements[i, 0] > maxMove:
                maxMove = pointsDeplacements[i, 0]
            if abs(pointsDeplacements[i, 0]) < minMove:
                minMove = abs(pointsDeplacements[i, 0])
            averageMove = ((averageMove * itMove) + pointsDeplacements[i, 1]) / (itMove + 1)
            itMove = itMove + 1
    averageMove = abs(averageMove)
    #print(type(pointsDeplacements))
    #print('minMove : ', minMove)
    #print('maxMove : ', maxMove)
    print('averageMove : ', averageMove)
    return

if __name__ == '__main__':

    video_source_path = "Inputs//T4_HFV_ManufactureMontluc.mp4"
    extract_image_one_fps(video_source_path)
    vidcap = cv2.VideoCapture(video_source_path)
    nb_frame = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    i = 1
    while i < nb_frame:

        # Read reference image : print("Reading reference image : ", refFilename)
        refFilename = "Outputs/frame%i.jpg" % i
        imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

        # Read image to be compared ; print("Reading image to align : ", imFilename);
        i = i + 1
        imFilename = "Outputs/frame%i.jpg" % i
        im = cv2.imread(imFilename, cv2.IMREAD_COLOR)

        GetDeplacement(im, imReference)


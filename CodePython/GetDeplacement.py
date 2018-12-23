from __future__ import print_function
import cv2
import numpy as np

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.8


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

    i = 1
    while i < 348:

        # Read reference image : print("Reading reference image : ", refFilename)
        refFilename = "Outputs/frame%i.jpg" % i
        imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

        # Read image to be compared ; print("Reading image to align : ", imFilename);
        i = i + 1
        imFilename = "Outputs/frame%i.jpg" % i
        im = cv2.imread(imFilename, cv2.IMREAD_COLOR)

        GetDeplacement(im, imReference)


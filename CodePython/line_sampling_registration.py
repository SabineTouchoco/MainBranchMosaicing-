import cv2
import numpy as np
from matplotlib import pyplot as plt

def creerMosaique(inputfilepath,outputPathName):
    # inputfilepath = "Inputs//T4_HFV_CollegeBellecombe.mp4"

    video = cv2.VideoCapture(inputfilepath)
    video2 = video
    fps = video.get(cv2.CAP_PROP_FPS)
    print('Video fps : ' + str(fps))

    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    print('Video width : ' + str(width))

    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('Video height : ' + str(height))

    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    print('Video frame count : ' + str(frame_count))

    count = 0
    center = int(width / 2)
    offset = 0

    hauteur_max = height - 0  # Ronge la partie du bas de l'image quand hauteur max augmente.
    hauteur_min = 00  # Ronge la partie du haut de l'image quand hauteur min augmente.

    delta_0 = 80.0
    coefLargeurBande = 3  # Doit etre compris entre 1 et 8.
    # 1 car on realise une operation : coefLargeurBande - 1 qui doit etre strictement positive
    # 1 aussi car on ne prend pas plus petit que la bande precedente.
    # 8 car la largeur totale(1920)*ratio image_remplissage_noir(1/3)/delta(80) = 4
    # au dela de 8, cela revient a la methode precedente sans covariance : prise de bande de lageur decroissante.

    for i in range(int(frame_count)):

        # Recherche de la ligne (n-1) dans l'image n.
        if count > 0:

            # Initialisation
            delta = delta_0 - (i - 1) * delta_0 / frame_count

            video2.set(cv2.CAP_PROP_POS_FRAMES, (i - 1))  # On cherche la ligne dans l'image (n+1).
            success_plus1, img = video2.read()
            img = img[int(hauteur_min):int(hauteur_max), :, :]
            if success_plus1:
                line = img[:, (center - int(coefLargeurBande * delta / 2)):(center + int(coefLargeurBande * delta / 2)),
                       :]  # On prend la ligne sur l'image (n-1).

                # Initialisation param
                success, img = video.read()  # On recupere l'image n. Objectif : chercher la meilleure correspondance avec la ligne (n-1).
                img = img[int(hauteur_min):int(hauteur_max), :, :]
                cv2.imwrite("Outputs//frame.jpg", img)
                img = cv2.imread("Outputs//frame.jpg", 0)
                img2 = img.copy()
                cv2.imwrite("Outputs//template_temp.jpg", line)
                template = cv2.imread("Outputs//template_temp.jpg", 0)  # line.copy()

                # Shape of image is accessed by img.shape.
                # It returns a tuple of number of rows, columns and channels (if image is color):
                # print img.shape
                # (342, 548, 3)
                try:  # Lecture de l'image OK
                    # print("img = " + str(type(img)))
                    w, h = template.shape[::-1]

                    # Choix de la methode
                    # All the 6 methods for comparison in a list
                    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR','cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
                    method = cv2.TM_CCORR_NORMED

                    # Application du "template Matching"
                    # Fait glisser l image du modele sur l image d'entree comme une convolution 2D
                    # et compare le modele et le patch de l'image d'entree.
                    res = cv2.matchTemplate(img, template, method)

                    # Trouve ou sont les valeurs maximum / minimum.
                    # Prenez le minimum ou maximum (selon methode) comme coin superieur gauche du rectangle.
                    # Prenez (w, h) comme largeur et hauteur du rectangle.
                    # Ce rectangle est la region du modele.
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                    # Si la methode est TM_SQDIFF ou TM_SQDIFF_NORMED, prendre le minimum comme coin superieur gauche du rectangle.
                    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                        top_left = min_loc
                    # Sinon prendre la maximum
                    else:
                        top_left = max_loc

                    # Definition du rectangle
                    # bottom_right = (top_left[0] + w, top_left[1] + h)
                    # Trace le rectangle sur img
                    # cv2.rectangle(img, top_left, bottom_right, 255, 2)

                    # Affichage du rectangle
                    # plt.subplot(131), plt.imshow(res, cmap='gray')
                    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                    # plt.subplot(132), plt.imshow(img, cmap='gray')
                    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                    # print("img " + str(i) + " sampled.")
                except:
                    pass
                success, img = video.read()

                if success:
                    img = img[int(hauteur_min):int(hauteur_max), :, :]

                    # Definition de la prochaine ligne
                    debutBande = coefLargeurBande - 1
                    debutBande = delta * debutBande / 2
                    debutBande = top_left[0] + debutBande
                    debutBande = int(debutBande)
                    finBande = coefLargeurBande + 1
                    finBande = delta * finBande / 2
                    finBande = top_left[0] + finBande
                    finBande = int(finBande)
                    nextLine = img[:, debutBande:finBande, :]
                else:
                    print("Erreur de lecture video ligne 109")

                # plt.subplot(133), plt.imshow(nextLine, cmap='gray')
                # plt.title('Bande suivante'), plt.xticks([]), plt.yticks([])
                # plt.suptitle(method)
                # plt.show()

                # img_path = "Outputs/result_delta_var.png"
                # cv2.imwrite(img_path, result)
                # print("Erreur de lecture d'image.")

        else:
            # Prendre toute la premiere moitie (droite) de l'image + delta
            # Pas de ligne a rechercher dans l'image !
            delta = delta_0 - i * delta_0 / frame_count
            # delta = int(delta)
            success, img = video.read()
            img = img[int(hauteur_min):int(hauteur_max), :, :]
            # V0
            nextLine = img[:, int(center - (delta / 2)):int(width) - int(width / 2.9), :]

        # Concatenation
        # success, img = video.read()
        # if success:
        # delta_0 = 80
        # delta = delta_0 - i * delta_0 / frame_count
        # success, img = video.read()
        # line = img[:, (center - delta + offset):(center + delta + offset), :]
        if count > 0:
            result = np.concatenate((nextLine, result), 1)
        else:
            result = nextLine
        # img_path = "outputs/img_" + str(count) + ".png"
        # cv2.imwrite(img_path, img)
        count += 1
        # print("img " + str(i) + " sampled.")
        # img_path = "Outputs/result_delta_var.png"
        # cv2.imwrite(img_path, result)

    # print("Done.")

    img_path = "Outputs/result.png"
    cv2.imwrite(outputPathName, result)

    # result = cv2.blur(result,(10,10))
    # img_path = "Outputs/filtered_result.png"
    # cv2.imwrite(img_path, result)

    print("Image saved.")
    return result

# ---------------------------------------------------------------------------------------------------------------------
# Debut du programme execute
# ---------------------------------------------------------------------------------------------------------------------

NomsVideos = ["T4_HFV_ArchivesDepartementales",
              "T4_HFV_CharpennesCharlesHernu",
              "T4_HFV_CollegeBellecombe",
              "T4_HFV_EtatsUnisMuseeTonyGarnier",
              "T4_HFV_GarePartDieuVillette",
              "T4_HFV_LeTonkin",
              "T4_HFV_LyceeLumiere",
              "T4_HFV_LyceeColbert",
              "T4_HFV_ManufactureMontluc",
              "T4_HFV_ProfesseurBeauvisageCISL",
              "T4_HFV_ThiersLafayette",
              "T4_HFV_UniversiteLyon1"]
#              "T4_HFV_LyceeColbert" "T4_HFV_JetDEauMendesFrance" = Videos ratees

for it_video in range(11,12):    # (0,11):
                                # 32.5 minutes pour 11 videos
    nomVideo = NomsVideos[it_video]
    print("Debut analyse de la video : " + nomVideo)
    inputfilepath = "Inputs//" + nomVideo + ".mp4"
    outputPathName = "Outputs//" + nomVideo + ".png"
    mon_image = creerMosaique(inputfilepath,outputPathName)

print("Done.")
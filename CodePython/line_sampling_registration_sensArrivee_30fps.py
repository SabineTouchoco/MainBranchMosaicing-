import cv2
import numpy as np
from matplotlib import pyplot as plt

# Fonction qui renvoit la position du point en haut a gauche de la ligne dans la nouvelle image
def rechercherLigneN_1DansN(delta_0,frame_count,video,video2,i,hauteur_min,hauteur_max,center,coefLargeurBande):
    # Initialisation
    delta = delta_0 - (i - 1) * delta_0 / frame_count
    top_left = [0,0]

    video2.set(cv2.CAP_PROP_POS_FRAMES, (i - 1))  # On cherche la ligne dans l'image (n+1).
    success_plus1, img = video2.read()

    if success_plus1:
        img = img[int(hauteur_min):int(hauteur_max), :, :]
        line = img[:, (center - int(coefLargeurBande * delta / 2)):(center + int(coefLargeurBande * delta / 2)),:]  # On prend la ligne sur l'image (n-1).

        # Initialisation param
        success, img = video.read()  # On recupere l'image n. Objectif : chercher la meilleure correspondance avec la ligne (n-1).
        if success:
            img = img[int(hauteur_min):int(hauteur_max), :, :]
            cv2.imwrite("Outputs//frame.jpg", img)
            img = cv2.imread("Outputs//frame.jpg", 0)
            cv2.imwrite("Outputs//template_temp.jpg", line)
            template = cv2.imread("Outputs//template_temp.jpg", 0)  # line.copy()

            try: # La lecture cv2 im read ne fonctionne pas sur une ou plusieurs frame a la fin.
                # Shape of image is accessed by img.shape.
                # It returns a tuple of number of rows, columns and channels (if image is color):
                # print img.shape
                # (342, 548, 3)
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
                print("Erreur lecture image pour correlation.")
        else:
            print("Erreur lecture video.")
    return top_left

# Definition de la prochaine ligne
def definirLigneAConcatener(img,hauteur_min,hauteur_max,coefLargeurBande,delta,top_left,sensArriveeAQuai):
    img = img[int(hauteur_min):int(hauteur_max), :, :]
    if sensArriveeAQuai == "QuaiADroite":
        debutBande = coefLargeurBande - 1
        debutBande = delta * debutBande / 2
        debutBande = top_left[0] + debutBande
        debutBande = int(debutBande)
        finBande = coefLargeurBande + 1
        finBande = delta * finBande / 2
        finBande = top_left[0] + finBande
        finBande = int(finBande)
        nextLine = img[:, debutBande:finBande, :]
    elif sensArriveeAQuai == "QuaiAGauche":
        debutBande = coefLargeurBande + 1
        debutBande = delta * debutBande / 2
        debutBande = top_left[0] + debutBande
        debutBande = int(debutBande)
        finBande = coefLargeurBande * delta
        finBande = top_left[0] + finBande
        finBande = int(finBande)
        nextLine = img[:, debutBande:finBande, :]
    return nextLine

def creerMosaique(cheminFichierEntree,cheminFichiersSortie,sensArriveeAQuai):

    #Lecture de la video
    video = cv2.VideoCapture(cheminFichierEntree)
    video2 = video

    # Affichage
    fps = video.get(cv2.CAP_PROP_FPS)
    print('Video fps : ' + str(fps))
    largeur = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    print('Largeur images : ' + str(largeur))
    hauteur = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('Hauteur images : ' + str(hauteur))
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    print('Video frame count : ' + str(frame_count))

    # Initialisation de la fonction
    count = 0
    center = int(largeur / 2)
    offset = 0
    if sensArriveeAQuai == "QuaiADroite":
        hauteur_max = hauteur - 0  # Ronge la partie du bas de l'image quand hauteur max augmente.
        hauteur_min = 00  # Ronge la partie du haut de l'image quand hauteur min augmente.
        delta_0 = 80.0
        coefLargeurBande = 3    # Doit etre compris entre 1 et 8.
                                # 1 car on realise une operation : coefLargeurBande - 1 qui doit etre strictement positive
                                # 1 aussi car on ne prend pas plus petit que la bande precedente.
                                # 8 car la largeur totale(1920)*ratio image_remplissage_noir(1/3)/delta(80) = 4
                                # au dela de 8, cela revient a la methode precedente sans covariance : prise de bande de lageur decroissante.
    elif sensArriveeAQuai == "QuaiAGauche":
        hauteur_max = hauteur/4  # Ronge la partie du bas de l'image quand hauteur max augmente.
        hauteur_max = hauteur - hauteur_max
        hauteur_min = hauteur/3  # Ronge la partie du haut de l'image quand hauteur min augmente.
        delta_0 = 0.6
        coefLargeurBande = 30
    else:  # Quai a gauche ou droite
        print("Erreur de choix de sensArriveeAQuai.")

    # Traitement image par image
    for i in range(int(frame_count)):
        if count > 0:
            top_left = rechercherLigneN_1DansN(delta_0,
                                               frame_count,
                                               video,
                                               video2,
                                               i,
                                               hauteur_min,
                                               hauteur_max,
                                               center,
                                               coefLargeurBande) # Recherche de la ligne (n-1) dans l'image n.

            success, img = video.read()
            if success:
                nextLine = definirLigneAConcatener(img,
                                                   hauteur_min,
                                                   hauteur_max,
                                                   coefLargeurBande,
                                                   delta,
                                                   top_left,
                                                   sensArriveeAQuai)
            else:
                print("Erreur de lecture video.")

            # plt.subplot(133), plt.imshow(nextLine, cmap='gray')
            # plt.title('Bande suivante'), plt.xticks([]), plt.yticks([])
            # plt.suptitle(method)
            # plt.show()

            # img_path = "Outputs/result_delta_var.png"
            # cv2.imwrite(img_path, result)
            # print("Erreur de lecture d'image.")

        else: # Traitement de la premiere image
            success, img = video.read()
            if success:
                if sensArriveeAQuai == "QuaiADroite":
                    # Prendre toute la premiere moitie (DROITE) de l'image + delta
                    # Pas de ligne a rechercher dans l'image !
                    delta = delta_0 - i * delta_0 / frame_count
                    img = img[int(hauteur_min):int(hauteur_max), :, :]
                    nextLine = img[:, int(center - (delta / 2)):int(largeur) - int(largeur / 2.9), :] # int(largeur / 2.9) = offset pour supprimer la bande noire sur le cote
                elif sensArriveeAQuai == "QuaiAGauche":
                    # Prendre toute la premiere moitie (GAUCHE) de l'image + delta
                    # Pas de ligne a rechercher dans l'image !
                    delta = delta_0 - i * delta_0 / frame_count
                    img = img[int(hauteur_min):int(hauteur_max), :, :]
                    nextLine = img[:, int(largeur / 2.9):int(center + (delta / 2)), :] # int(largeur / 2.9) = offset pour supprimer la bande noire sur le cote
            else:
                print("Erreur lecture Video.")
        # Concatenation
        if count > 0:
            if sensArriveeAQuai == "QuaiADroite":
                result = np.concatenate((nextLine, result), 1)
            elif sensArriveeAQuai == "QuaiAGauche":
                result = np.concatenate((result, nextLine), 1)
        else:
            result = nextLine
        count += 1
        # print("img " + str(i) + " sampled.")
        # img_path = "Outputs/result_delta_var.png"
        # cv2.imwrite(img_path, result)

    # img_path = "Outputs/result.png"
    cv2.imwrite(cheminFichiersSortie + ".png", result)

    result = cv2.blur(result,(4,4))
    # img_path = "Outputs/filtered_result.png"
    cv2.imwrite(cheminFichiersSortie + "_filtered.png", result)


    print("Image saved.")

    return result

# ---------------------------------------------------------------------------------------------------------------------
# Debut du programme execute
# ---------------------------------------------------------------------------------------------------------------------

NomsVideosQuaiADroite = ["02-valmy1",
                         "02-valmy2",
                         "05-bellecour1",
                         "05-bellecour2",
                         "11-grangeblanche1",
                         "11-grangeblanche2",
                         "11-grangeblanche3",
                         "T4_HFV_ArchivesDepartementales",
                         "T4_HFV_CharpennesCharlesHernu",
                         "T4_HFV_CollegeBellecombe",
                         "T4_HFV_EtatsUnisMuseeTonyGarnier",
                         "T4_HFV_GarePartDieuVillette",
                         "T4_HFV_LeTonkin",
                         "T4_HFV_LyceeLumiere",
                         "T4_HFV_ManufactureMontluc",
                         "T4_HFV_ProfesseurBeauvisageCISL",
                         "T4_HFV_ThiersLafayette",
                         "T4_HFV_UniversiteLyon1",
                         "VID_20181221_082322"]
#              "T4_HFV_LyceeColbert" "T4_HFV_JetDEauMendesFrance" = Videos ratees

NomsVideosQuaiAGauche = ["01-garevaise1",
                         "03-gorgeloup1",
                         "03-gorgeloup2",
                         "04-vieuxlyon1",
                         "04-vieuxlyon2",
                         "06-guillotiere1",
                         "06-guillotiere2",
                         "07-saxegambetta1",
                         "07-saxegambetta2",
                         "08-garibaldi1",
                         "08-garibaldi2",
                         "09-sanssouci1",
                         "09-sanssouci2",
                         "10-monplaisir1",
                         "10-monplaisir2",
                         "12-laennec1",
                         "12-laennec2",
                         "13-mermoz1",
                         "13-mermoz2",
                         "14-parilly1",
                         "14-parilly2",
                         "15-garevenissieux"]

sensArriveeAQuai = "QuaiADroite"

# nomVideo = "P1190069"
# print("Debut analyse de la video : " + nomVideo)
# cheminFichierEntree = "Inputs//" + nomVideo + ".MOV"
# cheminFichiersSortie = "Outputs//" + nomVideo
# mon_image = creerMosaique(cheminFichierEntree,cheminFichiersSortie,sensArriveeAQuai)

nomVideo = "20190119_144304"
print("Debut analyse de la video : " + nomVideo)
cheminFichierEntree = "Inputs//" + nomVideo + ".mp4"
cheminFichiersSortie = "Outputs//" + nomVideo
mon_image = creerMosaique(cheminFichierEntree,cheminFichiersSortie,sensArriveeAQuai)

for it_video in range(0,2):    # (7,19)
                                # 32.5 minutes pour 11 videos
    nomVideo = NomsVideosQuaiADroite[it_video]
    print("Debut analyse de la video : " + nomVideo)
    cheminFichierEntree = "Inputs//QuaiADroite//" + nomVideo + ".mp4"
    cheminFichiersSortie = "Outputs//" + nomVideo
    mon_image = creerMosaique(cheminFichierEntree,cheminFichiersSortie,sensArriveeAQuai)

sensArriveeAQuai = "QuaiAGauche"
for it_video in range(0,22):    # 32.5 minutes pour 11 videos
    nomVideo = NomsVideosQuaiAGauche[it_video]
    print("Debut analyse de la video : " + nomVideo)
    cheminFichierEntree = "Inputs//QuaiAGauche//" + nomVideo + ".mp4"
    cheminFichiersSortie = "Outputs//" + nomVideo
    mon_image = creerMosaique(cheminFichierEntree,cheminFichiersSortie,sensArriveeAQuai)

print("Done.")
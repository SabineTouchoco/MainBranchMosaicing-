import cv2
import numpy as np
from matplotlib import pyplot as plt

# Fonction permettant de tourner une image
def rotate_image(mat, angle):
    # mat = image devant etre tournee.
    # angle = angle de la rotation a effectuer.
    # Source de la fonction : https://stackoverflow.com/questions/43892506/opencv-python-rotate-image-without-cropping-sides

    height, width = mat.shape[:2] # image shape a 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D necessite des coordonnees dans l'ordre inverse (largeur, hauteur) par rapport a la forme

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # la rotation calcule le cos et le sinus, en prenant des absolus de ceux-ci.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # trouver les nouvelles limites de largeur et de hauteur
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # soustraire l'ancien centre d'image (ramenant l'image a l'origine) et ajoutez les coordonnees du nouveau centre d'image
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # faire pivoter l'image avec les nouvelles limites et la matrice de rotation translatee
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

# Fonction qui renvoit la position du point en haut a gauche de la ligne dans la nouvelle image.
# Recherche de la ligne (n-1) dans l'image n.
def rechercherLigneN_1DansN(imageVideo,bandeN_1):
    # imageVideo  = image sur laquelle on recherche la bande precedente.
    # bandeN_1    = bande a rechercher dans l'image actuelle.
                # = centre de l'image precedente + ((coefLargeurBande-1)/2) de chaque cote.

    # Initialisation
    top_left = [0, 0]

    # Necessite d'ecrire puis de lire l'image par rapport au format requis a l'execution des fonctions de correlation
    cv2.imwrite("Outputs//frame.jpg", imageVideo)
    imageCorrelation = cv2.imread("Outputs//frame.jpg", 0)
    cv2.imwrite("Outputs//template_temp.jpg", bandeN_1)
    template = cv2.imread("Outputs//template_temp.jpg", 0)  # line.copy()

    try:  # La lecture cv2 im read ne fonctionne pas sur une ou plusieurs frame a la fin.
        # La forme de l'image est accessible par img.shape.
        # Il retourne un tuple de nombre de lignes, de colonnes et de canaux (si image est couleur):
        # print img.shape
        # (342, 548, 3)
        w, h = template.shape[::-1]

        # Choix de la methode
        # methodes possibles = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = cv2.TM_CCORR_NORMED

        # Application du "template Matching"
        # Fait glisser l image du modele sur l image d'entree comme une convolution 2D
        # et compare le modele et le patch de l'image d'entree.
        res = cv2.matchTemplate(imageCorrelation, template, method)

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
    except:
        print("Erreur lecture image pour correlation.")

    return top_left

# Definition de la prochaine ligne
def definirLigneAConcatener(imageVideo,
                            coefLargeurBande,
                            delta,
                            top_left,
                            sensArriveeAQuai):
    # imageVideo  = image sur laquelle on recherche la bande precedente.
    # coefLargeurBande = multiple de la largeur de bande.
                # coefLargeurBande = largeur de bande cherchee / largeur de bande a prendre
                # Correspond a la zone recherchee dans les images par correlation.
                # Doit etre superieur a 1 car on realise une operation : coefLargeurBande - 1 qui doit etre strictement positive
                # (3 pour 30 fps et delta_0 = 80, 6 pour 60 fps et delta0 = 40)
    # delta = largeur de la bande a prendre.
    # top_left = position (en haut a gauche) ou la bande a ete trouvee dans l'image.
                # top_left[0] = largeur a partir de laquelle la bande a ete trouvee.
                # top_left[1] = 0 (dans notre cas) = hauteur a partir de laquelle la bande a ete trouvee.
    # sensArriveeAQuai = "QuaiADroite" ou "QuaiAGauche", definit dans quel ordre doivent etre concatener les bandes, la position de la prochaine bande a prendre par rapport a l'endroit ou la correlation est maximale.

    if sensArriveeAQuai == "QuaiADroite":
        debutBande = coefLargeurBande - 1
        debutBande = delta * debutBande / 2
        debutBande = top_left[0] + debutBande
        debutBande = int(debutBande)
        finBande = coefLargeurBande + 1
        finBande = delta * finBande / 2
        finBande = top_left[0] + finBande
        finBande = int(finBande)
        bandeN = imageVideo[:, debutBande:finBande, :]
    elif sensArriveeAQuai == "QuaiAGauche":
        debutBande = coefLargeurBande + 1
        debutBande = delta * debutBande / 2
        debutBande = top_left[0] + debutBande
        debutBande = int(debutBande)
        finBande = coefLargeurBande * delta
        finBande = top_left[0] + finBande
        finBande = int(finBande)
        bandeN = imageVideo[:, debutBande:finBande, :]
    return bandeN

def creerMosaique(cheminVideo,
                  delta_0,
                  hauteur_max,
                  hauteur_min,
                  coefLargeurBande,
                  sensArriveeAQuai,
                  rotationNecessaire,
                  cheminFichiersSortie):
    # cheminVideo = chemin complet de la video avec l'extension de la video
    # delta_0 = largeur initiale de la bande prise dans les images de la video
    # hauteur_max (entre 0 et 1) = ronge la partie du bas de l'image quand hauteur max augmente (la hauteur 0 est en haut de l'image!)
    # hauteur_min (entre 0 et 1, inferieur a hauteur_max) = Ronge la partie du haut de l'image quand hauteur min augmente.
    # coefLargeurBande = multiple de la largeur de bande.
                        # coefLargeurBande = largeur de bande cherchee / largeur de bande a prendre
                        # Correspond a la zone recherchee dans les images par correlation.
                        # Doit etre superieur a 1 car on realise une operation : coefLargeurBande - 1 qui doit etre strictement positive
                        # (3 pour 30 fps et delta_0 = 80, 6 pour 60 fps et delta0 = 40)
    # sensArriveeAQuai = "QuaiADroite" ou "QuaiAGauche", definit dans quel ordre doivent etre concatener les bandes, la position de la prochaine bande a prendre par rapport a l'endroit ou la correlation est maximale.
    # rotationNecessaire = 0,90,180 ou -90 si la video n'est pas dans le bon sens (personnes avec les pieds en bas) pour la reconstitution.
    # cheminFichiersSortie = emplacement ou sauvegarder les resultats (et ou sont enregistres des fichiers de travail de l'algorithme).

    # Verification de parametres
    if hauteur_max < hauteur_min:
        print("Erreur : hauteur_max doit etre superieur a hauteur_min.")
    if coefLargeurBande < 1:
        print("Erreur : coefLargeurBande doit etre superieur a 1.")
    if (sensArriveeAQuai != "QuaiAGauche") and (sensArriveeAQuai != "QuaiADroite"):
        print("Erreur de choix de sensArriveeAQuai.")
    if (rotationNecessaire!=0) and (rotationNecessaire!=90) and (rotationNecessaire!=180) and (rotationNecessaire!=-90):
        print("Erreur : rotationNecessaire doit etre egale a 0, 90, 180 ou -90 degres.")

    # Lecture de la video
    video = cv2.VideoCapture(cheminVideo)

    # Recuperation des parametres de la video
    fps = video.get(cv2.CAP_PROP_FPS)
    print('Video fps : ' + str(fps))
    if (rotationNecessaire==90) or (rotationNecessaire==-90):
        # ATTENTION ! Comme la video est prise en format portrait la largeur de l'image correspond a la hauteur de la video
        largeur = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print('Largeur images : ' + str(largeur))
        hauteur = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print('Hauteur images : ' + str(hauteur))
    else:
        # Pas de rotation a faire sur les image extraites de la video
        largeur = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print('Largeur images : ' + str(largeur))
        hauteur = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print('Hauteur images : ' + str(hauteur))
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    print('Video frame count : ' + str(frame_count))

    # Initialisation de la fonction
    center = int(largeur / 2) # Centre de l'image
    hauteur_max = hauteur*hauteur_max  # Ronge la partie du bas de l'image quand hauteur max augmente.
    hauteur_min = hauteur*hauteur_min  # Ronge la partie du haut de l'image quand hauteur min augmente.
    bandeN_1 = 0
    bandeN = 0

    # ---------------------------------------------------------------------------
    # Traitement image par image
    for i in range(int(frame_count)):
        # Initialisation pour l'image en cours de traitement
        delta = delta_0 - i * delta_0 / (frame_count*1.33) # Adaptation de la largeur de la bande a prendre en fonction du temps.
        success, imageVideo = video.read()
        if success:
            # Preparation de l'image pour le traitement : rotation, redimensionnement
            if (rotationNecessaire == 90) or (rotationNecessaire == -90):
                imageVideo = rotate_image(imageVideo, -90)
            imageVideo = imageVideo[int(hauteur_min):int(hauteur_max), :, :]

            # Si ce n'est pas la premiere image :
                    # 1 - On recherche la bande precedante.
                    # 2 - On identifie la bande a prendre.
                    # 3 - On ajoute concatenation) la bande a prendre avec la mosaique.
            if i > 0:
                # 1 - On recherche la bande precedante.
                top_left = rechercherLigneN_1DansN(imageVideo,
                                                   bandeN_1)  # Recherche de la ligne (n-1) dans l'image n.
                # 2 - On identifie la bande a prendre.
                bandeN = definirLigneAConcatener(imageVideo,
                                                 coefLargeurBande,
                                                 delta,
                                                 top_left,
                                                 sensArriveeAQuai)
                # 3 - On ajoute concatenation) la bande a prendre avec la mosaique.
                if sensArriveeAQuai == "QuaiADroite":
                    mosaique = np.concatenate((bandeN, mosaique), 1)
                elif sensArriveeAQuai == "QuaiAGauche":
                    mosaique = np.concatenate((mosaique, bandeN), 1)
                offset = coefLargeurBande*delta
            # Si on traite la premiere image : on prend la premiere moitie de l'image pour l'ajouter dans la mosaique.
            else:
                # 1 - On prend la premiere moitie de l'image pour l'ajouter dans la mosaique.
                if sensArriveeAQuai == "QuaiADroite":
                    # Prendre toute la premiere moitie (DROITE) de l'image + delta
                    # Pas de ligne a rechercher dans l'image !
                    bandeN = imageVideo[:, int(center - (delta / 2)):int(largeur),:]
                elif sensArriveeAQuai == "QuaiAGauche":
                    # Prendre toute la premiere moitie (GAUCHE) de l'image + delta
                    # Pas de ligne a rechercher dans l'image !
                    bandeN = imageVideo[:, 0:int(center + (delta / 2)),:]
                mosaique = bandeN
            # On initialise la bande a rechercher dans la prochaine image = bandeN_1
            bandeN_1 = imageVideo[:, int(center - (coefLargeurBande*delta/2)):int(center + (coefLargeurBande*delta/2)), :]
        else:
            # En cas de probleme lors de la lecture de l'image dans la video (success = 0 apres video.read()) on affiche un message d'erreur.
            print("Erreur lecture Video.")

    # ---------------------------------------------------------------------------
    # Fin de la boucle de traitement image par image.
        # On sauvegarde la mosaique en format PNG avec le chemin et nom de fichier specifies.
    cv2.imwrite(cheminFichiersSortie + ".png", mosaique)

    # Filtrage de l'image : filtre moyenneur pour supprimer les transitions trop brutales (lignes entre les bandes).
    # mosaique = cv2.blur(mosaique, (4, 4))
    # cv2.imwrite(cheminFichiersSortie + "_filtered.png", mosaique)

    return mosaique

# ---------------------------------------------------------------------------------------------------------------------
# Debut du programme execute
# ---------------------------------------------------------------------------------------------------------------------

NomsVideosQuaiADroiteMetroMp4 = ["02-valmy1",
                                 "02-valmy2",
                                 "05-bellecour1",
                                 "05-bellecour2",
                                 "11-grangeblanche1",
                                 "11-grangeblanche3"]

NomsVideosQuaiADroiteTramMp4 = ["T4_HFV_ArchivesDepartementales",
                                "T4_HFV_CharpennesCharlesHernu",
                                "T4_HFV_CollegeBellecombe",
                                "T4_HFV_EtatsUnisMuseeTonyGarnier",
                                "T4_HFV_GarePartDieuVillette",
                                "T4_HFV_JetDEauMendesFrance",
                                "T4_HFV_LeTonkin",
                                "T4_HFV_LyceeColbert",
                                "T4_HFV_LyceeLumiere",
                                "T4_HFV_ManufactureMontluc",
                                "T4_HFV_ProfesseurBeauvisageCISL",
                                "T4_HFV_ThiersLafayette",
                                "T4_HFV_UniversiteLyon1",
                                "VID_20181221_082322"]

NomsVideosQuaiADroiteTramMov = ["P1190070",
                                "P1190071",
                                "P1190072",
                                "P1190079",
                                "P1190080",
                                "P1190082",
                                "P1190083",
                                "P1190084",
                                "P1190085"]

NomsVideosQuaiAGaucheMov = ["P1190073",
                            "P1190074",
                            "P1190076",
                            "P1190078"]

NomsVideosQuaiAGaucheMp4 = ["01-garevaise1",
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

# Performance : 63 minutes pour 44 videos

# (0,6) = range pour analyser toutes les videos correspondantes.
for it_video in range(0,0):     # Probleme : la ligne au milieu de l'image ne comporte pas d'information.
                                # Donc la correlation avec la ligne du milieu echoue.
    nomVideo = NomsVideosQuaiADroiteMetroMp4[it_video]
    print("Debut analyse de la video : " + nomVideo)
    cheminVideo = "Inputs//QuaiADroite//Metro//" + nomVideo + ".mp4"
    cheminFichiersSortie = "Outputs//" + nomVideo
    # creerMosaique(cheminVideo,
    #                   delta_0,
    #                   hauteur_max,
    #                   hauteur_min,
    #                   coefLargeurBande,
    #                   sensArriveeAQuai,
    #                   rotationNecessaire,
    #                   cheminFichiersSortie)
    mon_image = creerMosaique(cheminVideo,10,0.75,0.33,5,"QuaiADroite",0,cheminFichiersSortie)

# (0,9) = range pour analyser toutes les videos correspondantes.
for it_video in range(0, 0):    # 32.5 minutes pour 11 videos
    nomVideo = NomsVideosQuaiADroiteTramMov[it_video]
    print("Debut analyse de la video : " + nomVideo)
    cheminVideo = "Inputs//QuaiADroite//Tram//" + nomVideo + ".MOV"
    cheminFichiersSortie = "Outputs//" + nomVideo
    # creerMosaique(cheminVideo,
    #                   delta_0,
    #                   hauteur_max,
    #                   hauteur_min,
    #                   coefLargeurBande,
    #                   sensArriveeAQuai,
    #                   rotationNecessaire,
    #                   cheminFichiersSortie)
    mon_image = creerMosaique(cheminVideo,100,1,0,3,"QuaiADroite",-90,cheminFichiersSortie)

# (0,14) = range pour analyser toutes les videos correspondantes.
for it_video in range(0,0):    # 32.5 minutes pour 11 videos
    nomVideo = NomsVideosQuaiADroiteTramMp4[it_video]
    print("Debut analyse de la video : " + nomVideo)
    cheminVideo = "Inputs//QuaiADroite//Tram//" + nomVideo + ".mp4"
    cheminFichiersSortie = "Outputs//" + nomVideo
    # creerMosaique(cheminVideo,
    #                   delta_0,
    #                   hauteur_max,
    #                   hauteur_min,
    #                   coefLargeurBande,
    #                   sensArriveeAQuai,
    #                   rotationNecessaire,
    #                   cheminFichiersSortie)
    mon_image = creerMosaique(cheminVideo,100,1,0,3,"QuaiADroite",0,cheminFichiersSortie)

# (0,22) = range pour analyser toutes les videos correspondantes.
for it_video in range(0,22):    # 32.5 minutes pour 11 videos
    nomVideo = NomsVideosQuaiAGaucheMp4[it_video]
    print("Debut analyse de la video : " + nomVideo)
    cheminVideo = "Inputs//QuaiAGauche//" + nomVideo + ".mp4"
    cheminFichiersSortie = "Outputs//" + nomVideo
    # creerMosaique(cheminVideo,
    #                   delta_0,
    #                   hauteur_max,
    #                   hauteur_min,
    #                   coefLargeurBande,
    #                   sensArriveeAQuai,
    #                   rotationNecessaire,
    #                   cheminFichiersSortie)
    mon_image = creerMosaique(cheminVideo, 0.6, 0.75, 0.33, 30, "QuaiAGauche", 0, cheminFichiersSortie)

# (0,4) = range pour analyser toutes les videos correspondantes.
for it_video in range(0,0):    # 32.5 minutes pour 11 videos
    nomVideo = NomsVideosQuaiAGaucheMov[it_video]
    print("Debut analyse de la video : " + nomVideo)
    cheminVideo = "Inputs//QuaiAGauche//" + nomVideo + ".MOV"
    cheminFichiersSortie = "Outputs//" + nomVideo
    # creerMosaique(cheminVideo,
    #                   delta_0,
    #                   hauteur_max,
    #                   hauteur_min,
    #                   coefLargeurBande,
    #                   sensArriveeAQuai,
    #                   rotationNecessaire,
    #                   cheminFichiersSortie)
    mon_image = creerMosaique(cheminVideo,100,1,0,3,"QuaiAGauche",-90,cheminFichiersSortie)

print("Done.")
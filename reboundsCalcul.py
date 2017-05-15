import cv2
import numpy as np
from calibrage_beamer import calibration_c as calibration


# Cree une fonction affine de type Y=M*X+H
# Xa,Ya,Xb,Yb sont les valeurs de 2 points
# Return m,h
def ptsToFonction(Xa,Ya,Xb,Yb):
    if((float(Xb)-float(Xa)) != 0):
        m = (float(Yb)-float(Ya))/(float(Xb)-float(Xa))
        h = float(Yb)-(float(m)*float(Xb))
        return m, h
    else:
        m=0
        h = float(Yb) - (float(m) * float(Xb))
        return m,h

def whereIsCrossing(XaDroite, YaDroite, XbDroite, YbDroite):
        coordonnes = {}
        m, h = ptsToFonction(XaDroite, YaDroite, XbDroite, YbDroite)
        coordonnes["m"] = m
        coordonnes["h"] = h
        # droite horizontale du haut
        # y = 0 pour n'importe quelle valeur de x
        # x = laVariable
        ##mHaut, hHaut = ptsToFonction(0,0,MAX_X,0)
        # mHaut = 0
        # hHaut = 0
        # y = mDroite * x + hDroite
        # y = mHaut * x + hHaut
        # mHaut * x + hHaut = mDroite * x + hDroite
        # mHaut * x = mDroite * x + hDroite - hHaut
        yHaut = 0
        xHaut = h / m * -1
        coordonnes["yHaut"] = yHaut
        coordonnes["xHaut"] = xHaut
        # droite horizontale du bas
        # y = MAX_Y pour n'importe quelle valeur de x
        # x = laVariable
        # mBas, hBas = ptsToFonction(0, MAX_Y, MAX_X, MAX_Y)
        # mBas = 0
        # hBas = MAX_Y
        yBas = MAX_Y
        xBas = (yBas - h) / m
        coordonnes["yBas"] = yBas
        coordonnes["xBas"] = xBas
        # xBas = (hBas - h) / (mBas - m)

        # droite verticale de gauche
        # y = laVariable
        # x = 0 pour n'importe quelle valeur de y
        # mGauche, hGauche = ptsToFonction(0, 0, 0, MAX_Y)
        xGauche = 0
        yGauche = m * xGauche + h
        coordonnes["yGauche"] = yGauche
        coordonnes["xGauche"] = xGauche
        # droite verticale de droite
        # y = laVariable
        # x = MAX_X pour n'importe quelle valeur de y
        # mDroite, hDroite = ptsToFonction(MAX_X, 0, MAX_X, MAX_Y)
        xDroite = MAX_X
        yDroite = m * xDroite + h
        coordonnes["yDroite"] = yDroite
        coordonnes["xDroite"] = xDroite

        #print("Haut : X : " + str(xHaut) + " Y : " + str(yHaut))
        #print("Bas : X : " + str(xBas) + " Y : " + str(yBas))
        #print("Gauche X : : " + str(xGauche) + " Y : " + str(yGauche))
        #print("Droite X : : " + str(xDroite) + " Y : " + str(yDroite))

        return coordonnes

def rebond(pboule,pc0,*ptsPreced):
    coordonnes = whereIsCrossing(pboule[0], pboule[1], pc0[0], pc0[1])
    #print "coordonnes"
    #print coordonnes
    point1 = {"x": coordonnes["xHaut"], "y": coordonnes["yHaut"], "m": coordonnes["m"], "h": coordonnes["h"]}
    point2 = {"x": coordonnes["xBas"], "y": coordonnes["yBas"], "m": coordonnes["m"], "h": coordonnes["h"]}
    point3 = {"x": coordonnes["xDroite"], "y": coordonnes["yDroite"], "m": coordonnes["m"], "h": coordonnes["h"]}
    point4 = {"x": coordonnes["xGauche"], "y": coordonnes["yGauche"], "m": coordonnes["m"], "h": coordonnes["h"]}
    ps = {"point1": point1, "point2": point2, "point3": point3, "point4": point4}  # possible points
    #print ps
    #MAX_Y = 535
    #MAX_X = 1280
    MIN_Y = 0
    MIN_X = 0

    pps = []  # pertinent points
    for p in ps.values():
        if p["x"] <= MAX_X and p["x"] >= MIN_X and p["y"] <= MAX_Y and p["y"] >= MIN_Y:
            pps.append(p)

    pth = {}  # point to have
    if ptsPreced:
        #print "Yo nigga 3000"
        #print ptsPreced

        for pp in pps:
            if(not(int(pp["x"]) == int(ptsPreced[0]["x"]) and int(pp["y"]) == int(ptsPreced[0]["y"]))):
                pth = pp
    else:
        if (pboule[0] > pc0[0]):
            for pp in pps:
                if (pp["x"] > pboule[0]):
                    pth = pp
        else:
            for pp in pps:
                if (pp["x"] < pboule[0]):
                    pth = pp

    #print "start"
    #print pps
    #print "end"
    #print pth
    #print "pth"
    #print pth
    return pth
# Retourne les coordonnees de l'endroit ou ira taper la boule sur un cote du billard
# valeur permet de connaitre sur quelle cote tapera la boule
# coorX1 coorY1 sont les (premieres) coordonees (boule)
# coorX2 coorY2 sont les (deuxiemes) coordonees (queue)
# Return pt1x pt1y (les coordonnes du points)
def anglePosition(coorX1,coorY1,coorX2,coorY2,valeur):
    if (coorY1 < coorY2):
        if (valeur < 0 or valeur > MAX_X):
            # on test la position X de la boule par rapport a la position X de la queue
            # si la position X de la boule est superier a la position X de la queue alors la boule ira a droite
            if (coorX1 > coorX2):
                mQueue, hQueue = ptsToFonction(coorX2, coorY2, coorX1, coorY1)
                # X = MAX_X
                # Y = mQueue * MAX_X + hQueue
                Y = mQueue * MAX_X + hQueue
                # cv2.line(img, (pc0[0], pc0[1]), (MAX_X, int(Y)), (210, 0, 0), 1)

                #calcul des coordones pour le prochain rebonds
                #points au dessus de la normal Y
                if(coorY2 > int(Y)):
                    ptsImage = int(Y) - (abs(coorY2 - int(Y)))/2
                #points au dessous de la normal Y
                else :
                    ptsImage = int(Y) + (abs(coorY2 - int(Y)))/2

                #print 'droite'
                return MAX_X, int(Y),coorX1,ptsImage
            # gauche
            else:
                mQueue, hQueue = ptsToFonction(coorX2, coorY2, coorX1, coorY1)
                # X = 0
                # Y = mQueue * 0 + hQueue
                Y = mQueue * 0 + hQueue
                # cv2.line(img, (pc0[0], pc0[1]), (0, int(Y)), (210, 0, 0), 1)

                # calcul des coordones pour le prochain rebonds
                # points au dessus de la normal Y
                if (coorY2 > int(Y)):
                    ptsImage = int(Y) - (abs(coorY2 - int(Y)))/2
                # points au dessous de la normal Y
                else:
                    ptsImage = int(Y) + (abs(coorY2 - int(Y)))/2

                #print 'gauche'
                return 0, int(Y), coorX1, ptsImage
        # dans ce cas, la boule ira taper contre le haut
        else:
            mQueue, hQueue = ptsToFonction(coorX2, coorY2, coorX1, coorY1)
            # Y = 0
            # 0 = mQueue * X + hQueue
            if (mQueue == 0):
                X = -hQueue
            else:
                X = -hQueue / mQueue
            # cv2.line(img, (pc0[0], pc0[1]), (int(X), 0), (210, 0, 0), 1)

            # calcul des coordones pour le prochain rebonds
            # points a droite de la normal x
            if (coorX2 > int(X)):
                ptsImage = int(X) - (abs(coorX2 - int(X)))/2
            # points a gauche de la normal x
            else:
                ptsImage = int(X) + (abs(coorX2 - int(X)))/2

            #print 'haut'
            return int(X), 0,ptsImage,coorY1
    # ces directions possibles : bas, droite, gauche
    else:
        if (valeur < 0 or valeur > MAX_X):
            # on test la position X de la boule par rapport a la position X de la queue
            # si la position X de la boule est superier a la position X de la queue alors la boule ira a droite
            if (coorX1 > coorX2):
                mQueue, hQueue = ptsToFonction(coorX2, coorY2, coorX1, coorY1)
                # X = MAX_X
                # Y = mQueue * MAX_X + hQueue
                Y = mQueue * MAX_X + hQueue
                # cv2.line(img, (pc0[0], pc0[1]), (MAX_X, int(Y)), (210, 0, 0), 1)

                # calcul des coordones pour le prochain rebonds
                # points au dessus de la normal Y
                if (coorY2 > int(Y)):
                    ptsImage = int(Y) - (abs(coorY2 - int(Y)))/2
                # points au dessous de la normal Y
                else:
                    ptsImage = int(Y) + (abs(coorY2 - int(Y)))/2

                #print 'droite'
                return MAX_X, int(Y), coorX1, ptsImage
            # gauche
            else:
                mQueue, hQueue = ptsToFonction(coorX2, coorY2, coorX1, coorY1)
                # X = 0
                # Y = mQueue * 0 + hQueue
                Y = mQueue * 0 + hQueue
                # cv2.line(img, (pc0[0], pc0[1]), (0, int(Y)), (210, 0, 0), 1)

                # calcul des coordones pour le prochain rebonds
                # points au dessus de la normal Y
                if (coorY2 > int(Y)):
                    ptsImage = int(Y) - (abs(coorY2 - int(Y)))/2
                # points au dessous de la normal Y
                else:
                    ptsImage = int(Y) + (abs(coorY2 - int(Y)))/2

                #print 'gauche'
                return 0, int(Y), coorX1, ptsImage
        # dans ce cas, la boule ira taper contre le bas
        else:
            mQueue, hQueue = ptsToFonction(coorX2, coorY2, coorX1, coorY1)
            # Y = MAX_Y
            # MAX_Y = mQueue * X + hQueue
            if (mQueue == 0):
                X = (MAX_Y - hQueue)
            else:
                X = (MAX_Y - hQueue) / mQueue
            # cv2.line(img, (pc0[0], pc0[1]), (int(X), MAX_Y), (210, 0, 0), 1)

            if (coorX2 > int(X)):
                ptsImage = int(X) - (abs(coorX2 - int(X)))/2
            # points a gauche de la normal x
            else:
                ptsImage = int(X) + (abs(coorX2 - int(X)))/2

            #print 'bas'
            return int(X), MAX_Y, ptsImage, coorY1

#heigth = -180
#width = -1920


def graficalReturn(pboule,pc0) :
    global heigth
    global width
    global MAX_X
    global MAX_Y
    # Valeur en dur pour les tests, base sur des valeurs retournees par le
    # programmes qui va appeler cette futur fonction
    #backup
    #longueur et largeur de la surface de jeu
    MAX_X = calibration.width
    MAX_Y = calibration.heigth

    #position de la fenetre
    heigth = calibration.pos_x
    width =  calibration.pos_y

    pp0 = [0,0]       # points haut gauche
    pp1 = [MAX_X,0]     # points haut droite
    pp2 = [MAX_X,MAX_Y]      # points bas droite
    pp3 = [0,MAX_Y]      # points bas gauche

    #p0 = [640, 545]  # points haut gauche
    #p1 = [1920, 545]  # points haut droite
    #p2 = [1920, 1080]  # points bas droite
    #p3 = [640, 1080]  # points bas gauche

    #pboule = [700,100]  # Coordonnees de la boule blanche

    #pc0 = [640,360] # Premiere coordonee de la canne
    ##pc1 = [826,273] # Seconde coordonee de la canne

    # Create a black image
    #img = np.zeros((MAX_Y,MAX_X,3), np.uint8)
    #dessine la surface de jeu ainsi que du noir autour pour que le beamer n'affiche pas de lumiere
    img = np.zeros((1080,1920,3), np.uint8)

    # Dessine le pourtour de la zone de jeu
    cv2.line(img, (pp0[0], pp0[1]), (pp1[0], pp1[1]), (255, 0, 255), 5)
    cv2.line(img, (pp1[0], pp1[1]), (pp2[0], pp2[1]), (255, 0, 255), 5)
    cv2.line(img, (pp2[0], pp2[1]), (pp3[0], pp3[1]), (255, 0, 255), 5)
    cv2.line(img, (pp3[0], pp3[1]), (pp0[0], pp0[1]), (255, 0, 255), 5)


    # Dessine le pourtour de la zone de jeu
    #cv2.line(img,(p0[0],p0[1]),(p1[0],p1[1]),(0,0,255),5)
    #cv2.line(img,(p1[0],p1[1]),(p2[0],p2[1]),(0,0,255),5)
    #cv2.line(img,(p2[0],p2[1]),(p3[0],p3[1]),(0,0,255),5)
    #cv2.line(img,(p3[0],p3[1]),(p0[0],p0[1]),(0,0,255),5)

    # Dessine la boule blanche sur la zone de jeu
    cv2.circle(img,(pboule[0],pboule[1]), 55, (0,0,255), 20)

    #dessine la canne
    #cv2.line(img,(pc0[0],pc0[1]),(pc1[0],pc1[1]),(0,255,0),1)
    #dessine une boule pour representer le bout de la canne, la deuxieme coordonee arrivera plus tard dans le projet
    #cv2.circle(img,(pc0[0],pc0[1]), 10, (120,120,120), -1)
    """
    yHaut = 0 # peu importe la valeur x on a toujours le meme y
    xDroite = MAX_X # peu importe la valeur y on a toujours le meme x
    yBas = MAX_Y # peu importe la valeur x on a toujours le meme y
    xGauche = 0 # peu importe la valeur y on a toujours le meme x

    print yHaut
    print xDroite
    print yBas
    print xGauche
    """
    #print '----------------------'

    #test si la droite du haut est coupee correctement
    #mQueue,hQueue = ptsToFonction(pc0[0],pc0[1],pboule[0],pboule[1])
    # Y = 0
    # 0 = mQueue * X + hQueue
    #X = -hQueue/mQueue
    #cv2.line(img, (pc0[0],pc0[1]), (int(X),0), (210, 0, 0), 1)
    #print mQueue, hQueue, X

    #test si la droite de droite est coupee correctement
    #mQueue,hQueue = ptsToFonction(pc0[0],pc0[1],pboule[0],pboule[1])
    # X = MAX_X
    # Y = mQueue * MAX_X + hQueue
    #Y = mQueue * MAX_X + hQueue
    #cv2.line(img, (pc0[0],pc0[1]), (MAX_X,int(Y)), (210, 0, 0), 1)
    #print mQueue, hQueue, Y

    #test si la droite du bas est coupee correctement
    #mQueue,hQueue = ptsToFonction(pc0[0],pc0[1],pboule[0],pboule[1])
    # Y = MAX_Y
    # MAX_Y = mQueue * X + hQueue
    #X = (MAX_Y-hQueue)/mQueue
    #cv2.line(img, (pc0[0],pc0[1]), (int(X),MAX_Y), (210, 0, 0), 1)
    #print mQueue, hQueue, X

    #test si la droite de gauche est coupee correctement
    #mQueue,hQueue = ptsToFonction(pc0[0],pc0[1],pboule[0],pboule[1])
    # X = 0
    # Y = mQueue * 0 + hQueue
    #Y = mQueue * 0 + hQueue
    #cv2.line(img, (pc0[0],pc0[1]), (0,int(Y)), (210, 0, 0), 1)
    #print mQueue, hQueue, Y

    #print '----------------------'
    #----------------------------------------------------------------------------------------------------------------------

    # ******************************************************************************
    # Dessine le trait de la boule / canne jusqu'a l'angle du billard
    # ******************************************************************************
    #cette valeur est utilise pour savoir si nous sommes ou non dans la range de 0 - MAX_X
    mQueue,hQueue = ptsToFonction(pc0[0],pc0[1],pboule[0],pboule[1])

    valeur = (MAX_Y-hQueue)/ mQueue # c'est la valeur retournee par la fonction d'avant (X ou Y)

    #print 'valeur', valeur
    #print 'valeur1', valeur1
    # si la coordonnee Y de la boule est inferieur a celle de la queue alors la boule (donc la boule est au dessus de la queue) ira potentiellement dans
    # ces directions possibles : haut, droite, gauche
    #print valeur
    pt1x,pt1y,pt2x,pt2y=anglePosition(pboule[0],pboule[1],pc0[0],pc0[1],valeur)
    cv2.circle(img,(int(pt1x),int(pt1y)),12,(224,167,0),-1)

    #trace un trait bleu de la queue a la boule
    cv2.line(img, (pboule[0], pboule[1]), (pc0[0], pc0[1]), (210, 0, 0), 5)
    #trace un trait de la boule jusqu'a l'endroit ou aura lieu le rebond
    cv2.line(img, (pc0[0], pc0[1]), (pt1x, pt1y), (128, 0, 128), 2)
    #trace un trait du point de rebond jusqu'a l'endroit "suivant"
    #   mQueue, hQueue = ptsToFonction(pt1x, pt1y, pt2x, pt2y)
    #-------------------------------------------------------------------------------------------------------------------
    rebond1 = rebond(pboule, pc0)
    #cv2.circle(img,(int(rebond1["x"]),int(rebond1["y"])), 55, (0,240,20), 20)

    try:
        #temp = {"m": rebond1["m"] * -1}
        temp = {}
        temp ["m"] = rebond1["m"] * -1
        temp ["h"] = rebond1["y"] - temp["m"] * rebond1["x"]
        temp ["x"] = 10
        temp ["y"] = temp["m"] * temp["x"] + temp["h"]
        point3 = [0, 0]
        point3[0] = temp["x"]
        point3[1] = temp["y"]

        temp["h"] = rebond1["y"] - temp["m"] * rebond1["x"]
        temp["x"] = 100
        temp["y"] = temp["m"] * temp["x"] + temp["h"]
        point4 = [0, 0]
        point4[0] = temp["x"]
        point4[1] = temp["y"]

        rebond2 = rebond(point4, point3, rebond1)
        #-------------------------------------------------------------------------------------------------------------------
        #cv2.circle(img, (int(rebond2["x"]), int(rebond2["y"])), 55, (0, 240, 20), 20)

        temp = {"m": rebond2["m"] * -1}

        temp["h"] = rebond2["y"] - temp["m"] * rebond2["x"]
        temp["x"] = 10
        temp["y"] = temp["m"] * temp["x"] + temp["h"]
        point5 = [0, 0]
        point5[0] = temp["x"]
        point5[1] = temp["y"]

        temp["h"] = rebond2["y"] - temp["m"] * rebond2["x"]
        temp["x"] = 100
        temp["y"] = temp["m"] * temp["x"] + temp["h"]
        point6 = [0, 0]
        point6[0] = temp["x"]
        point6[1] = temp["y"]

        rebond3 = rebond(point6, point5, rebond2)
    except :
        pass
        #print "Le try catch des familles"
    #cv2.circle(img,(int(point3[0]),int(point3[1])), 55, (120,0,75), 5)
    #cv2.circle(img,(int(point4[0]),int(point4[1])), 55, (120,0,75), 5)

    try:
        #cv2.circle(img,(int(rebond2["x"]),int(rebond2["y"])), 15, (10,38,165), -1)
        cv2.line(img,(int(rebond1["x"]),int(rebond1["y"])),(int(rebond2["x"]),int(rebond2["y"])),(128,0,128), 5)
        cv2.line(img,(int(rebond2["x"]),int(rebond2["y"])),(int(rebond3["x"]),int(rebond3["y"])),(128,0,128), 5)
    except:
        #print "Auke lui aussi il est cool"
        pass

    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)

    # Position parfaite :3  (-2450, -700)

    key = cv2.waitKey(1)

    # print key

    if key == calibration.i:
        calibration.compteur = 1
    if key == calibration.o:
        calibration.compteur = 10
    if key == calibration.p:
        calibration.compteur = 100

    if key == calibration.w:
        calibration.pos_y -= calibration.compteur
    if key == calibration.s:
        calibration.pos_y += calibration.compteur

    if key == calibration.a:
        calibration.pos_x -= calibration.compteur
    if key == calibration.d:
        calibration.pos_x += calibration.compteur

    img = cv2.flip(img,0)
    img = cv2.flip(img,1)

    #print "avant affichage %s %s " % (calibration.pos_x, calibration.pos_y)

    print "calibration.pos_x : %s, calibration.pos_y : %s" % (calibration.pos_x, calibration.pos_y)

    cv2.moveWindow("image", calibration.pos_x, calibration.pos_y)  # envers
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("image", img)
    cv2.waitKey(1)
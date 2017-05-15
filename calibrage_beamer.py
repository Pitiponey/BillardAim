import cv2
import numpy as np


class calibration_c():
    heigth    =     473
    width     =     961
    pos_x     =   -1485
    pos_y     =      77
    compteur  =      10

    up        = 2490368
    down      = 2621440
    left      = 2424832
    rigth     = 2555904
    exit      =      27
    w         =     119
    a         =      97
    s         =     115
    d         =     100
    r         =     114
    i         =     105
    o         =     111
    p         =     112

def calibration():

    while 1:
        key = cv2.waitKey(0)


        if key == calibration_c.i:
            calibration_c.compteur =   1
        if key == calibration_c.o:
            calibration_c.compteur =  10
        if key == calibration_c.p:
            calibration_c.compteur = 100
        #print key
        if key == calibration_c.up:
            calibration_c.heigth -= calibration_c.compteur
        if key == calibration_c.down:
            calibration_c.heigth += calibration_c.compteur

        if key == calibration_c.left:
            calibration_c.width -= calibration_c.compteur
        if key == calibration_c.rigth:
            calibration_c.width += calibration_c.compteur

        if key == calibration_c.w:
            calibration_c.pos_y -= calibration_c.compteur
        if key == calibration_c.s:
            calibration_c.pos_y += calibration_c.compteur

        if key == calibration_c.a:
            calibration_c.pos_x -= calibration_c.compteur
        if key == calibration_c.d:
            calibration_c.pos_x += calibration_c.compteur

        if key == calibration_c.r:
            cv2.destroyAllWindows()
            print calibration_c.heigth, calibration_c.width, calibration_c.pos_x, calibration_c.pos_y
            break
            #return [calibration_c.heigth, calibration_c.width, calibration_c.pos_x, calibration_c.pos_y]

        img = np.zeros((calibration_c.heigth, calibration_c.width, 3), np.uint8)
        cv2.rectangle(img, (0, 0), (calibration_c.width, calibration_c.heigth), (255, 255, 255), -1)
        cv2.line(img, (1, 1), (1700, 1), (0, 0, 255), 3)


        cv2.imshow("Ajustage beamer", img)
        cv2.moveWindow("Ajustage beamer", calibration_c.pos_x, calibration_c.pos_y)
        cv2.setWindowProperty("Ajustage beamer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

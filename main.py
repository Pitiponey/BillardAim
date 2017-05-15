from calibrage_beamer import calibration
from WhiteBallDetect import white_ball_return
from cueDetecion import cue_position
from reboundsCalcul import graficalReturn
from cropTable import calcul
from configuration import configuration as config
from calibrage_beamer import calibration_c as calib

import numpy as np
import cv2

calibration()

pourtour_billard = calcul()


pts1 = np.float32([[pourtour_billard[0], pourtour_billard[1]],  # Hauf gauche
                   [pourtour_billard[2], pourtour_billard[3]],  # Haut droite
                   [pourtour_billard[4], pourtour_billard[5]],  # Bas gauche
                   [pourtour_billard[6], pourtour_billard[7]]]) # Bas Droite

pts2 = np.float32([[0, 0], [calib.width, 0], [0, calib.heigth], [calib.width, calib.heigth]])

cam = cv2.VideoCapture(config.CAMERA)
cam.set(3, 1280)
cam.set(4,  720)

#cam.set(3, 1280)
#cam.set(4, 535)

while 1:
    _, img = cam.read()
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (calib.width, calib.heigth))

    white_ball_position = white_ball_return(dst)
    cue_position_values = cue_position(dst)

    if cue_position_values != None:
        if white_ball_position != None:
            graficalReturn(white_ball_position, cue_position_values)
        else:
            print "Pas de cercle"
    else:
        print "Pas de queue"

    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()

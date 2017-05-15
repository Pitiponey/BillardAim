import cv2
import math
import numpy as np
from calibrage_beamer import calibration_c as calib

def cue_position(img_nomal):
    # converting to HSV
    hsv = cv2.cvtColor(img_nomal, cv2.COLOR_BGR2HSV)

    # Normal masking algorithm
    lower_blue = np.array([160, 120, 190])
    upper_blue = np.array([180, 210, 240])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(img_nomal, img_nomal, mask=mask)
    imgray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(imgray, 20, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("J'en sais rien", result)
    try:
        # pour chaque contour dans la liste des contours
        for contour in contours:
            # taille et perimetre
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)

            if area > 20 and perimeter > 20:
                red_point = tuple(contour[contour[:, :, 0].argmin()][0])
                green_point = tuple(contour[contour[:, :, 0].argmax()][0])
                blue_point = tuple(contour[contour[:, :, 1].argmin()][0])
                grey_point = tuple(contour[contour[:, :, 1].argmax()][0])

                # Calcul de la longeur
                red_length = int(math.sqrt(math.pow(red_point[0], 2) + math.pow(red_point[1], 2)))
                green_length = int(math.sqrt(math.pow(green_point[0], 2) + math.pow(green_point[1], 2)))
                blue_length = int(math.sqrt(math.pow(blue_point[0], 2) + math.pow(blue_point[1], 2)))
                grey_length = int(math.sqrt(math.pow(grey_point[0], 2) + math.pow(grey_point[1], 2)))

                list1 = [red_length, green_length, blue_length, grey_length]
                list1 = [int(x) for x in list1]
                list1.sort()

                # Devant
                point_queue_avant_X = 0
                point_queue_avant_Y = 0

                # Derriere
                point_queue_arriere_X = 0
                point_queue_arriere_Y = 0

                if list1[0] == red_length:
                    point_queue_avant_X = red_point[0]
                    point_queue_avant_Y = red_point[1]
                elif list1[0] == green_length:
                    point_queue_avant_X = green_point[0]
                    point_queue_avant_Y = green_point[1]
                elif list1[0] == blue_length:
                    point_queue_avant_X = blue_point[0]
                    point_queue_avant_Y = blue_point[1]
                else:
                    point_queue_avant_X = grey_point[0]
                    point_queue_avant_Y = grey_point[1]

                if list1[1] == red_length:
                    point_queue_avant_X = red_point[0]
                    point_queue_avant_Y = red_point[1]
                elif list1[1] == green_length:
                    point_queue_avant_X = green_point[0]
                    point_queue_avant_Y = green_point[1]
                elif list1[1] == blue_length:
                    point_queue_avant_X = blue_point[0]
                    point_queue_avant_Y = blue_point[1]
                else:
                    point_queue_avant_X = grey_point[0]
                    point_queue_avant_Y = grey_point[1]

                if list1[2] == red_length:
                    point_queue_arriere_X = red_point[0]
                    point_queue_arriere_Y = red_point[1]
                elif list1[2] == green_length:
                    point_queue_arriere_X = green_point[0]
                    point_queue_arriere_Y = green_point[1]
                elif list1[2] == blue_length:
                    point_queue_arriere_X = blue_point[0]
                    point_queue_arriere_Y = blue_point[1]
                else:
                    point_queue_arriere_X = grey_point[0]
                    point_queue_arriere_Y = grey_point[1]

                if list1[3] == red_length:
                    point_queue_arriere_X = red_point[0]
                    point_queue_arriere_Y = red_point[1]
                elif list1[3] == green_length:
                    point_queue_arriere_X = green_point[0]
                    point_queue_arriere_Y = green_point[1]
                elif list1[3] == blue_length:
                    point_queue_arriere_X = blue_point[0]
                    point_queue_arriere_Y = blue_point[1]
                else:
                    point_queue_arriere_X = grey_point[0]
                    point_queue_arriere_Y = grey_point[1]

                #print point_queue_avant_X, point_queue_avant_Y

                return point_queue_avant_X, point_queue_avant_Y

    except IndexError:
        print "Erreur : Pas de points detectes"


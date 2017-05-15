import cv2
from configuration import configuration as config

#mesure_pour_moyenne_boule_blanche = 0
#somme_mesure_boule_blanche = 0.

def white_ball_return(dst):
    # Our operations on the frame come here
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (2, 2))
    ret, thresh = cv2.threshold(blur, 200, 255, 0)

    circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=75, param2=10, minRadius=int(config.MIN_BALL_WIDTH), maxRadius=int(config.MAX_BALL_WIDTH)) #diametre moyen de la boule : 16.136

    mid_circle = [0, 1]
    if not circles == None:
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(dst, (i[0], i[1]), i[2], (255, 255, 0), 2)

            """global mesure_pour_moyenne_boule_blanche
            global somme_mesure_boule_blanche

            if mesure_pour_moyenne_boule_blanche < 2000:
                somme_mesure_boule_blanche += i[2]
                mesure_pour_moyenne_boule_blanche += 1
                print mesure_pour_moyenne_boule_blanche

            else:
                print somme_mesure_boule_blanche / mesure_pour_moyenne_boule_blanche
                fichier = open("moyenne_boule_blanche.txt", "w")
                fichier.write("Somme totale : " + str(somme_mesure_boule_blanche) + " \nNombre de mesures : " + str(mesure_pour_moyenne_boule_blanche)
                              + " \nMoyenne : " + str(somme_mesure_boule_blanche / mesure_pour_moyenne_boule_blanche))
            """

            # draw the center of the circle
            cv2.circle(dst, (i[0], i[1]), 2, (255, 0, 0), 3)

            mid_circle[0] = (i[0])
            mid_circle[1] = (i[1])

            cv2.imshow("circles", dst)
            return mid_circle

            # Display the resulting frame

    else:
       return None

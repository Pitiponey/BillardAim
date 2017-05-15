import cv2
from configuration import configuration as config

cam = cv2.VideoCapture(config.CAMERA)
cam.set(3, 1280)
cam.set(4, 720)

pointsSouris = []

def click_and_crop(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        print "LButtonDown %s %s" % (x, y)
        if len(pointsSouris) < 4:
            pointsSouris.append([x, y])


# Fonction inutile :)
def nothing(x):
    pass

# Dessins les cercle en prenant les valeurs des trackbars
def draw_circle(positionXY, listeCouleur):
    imageinchange = cv2.imread("captureForBordsDetectopm.jpg")

    color = listeCouleur[0]
    cv2.circle(imageinchange, (positionXY[0], positionXY[1]), 10, color, -1)

    color = listeCouleur[1]
    cv2.circle(imageinchange, (positionXY[2], positionXY[3]), 10, color, -1)

    color = listeCouleur[2]
    cv2.circle(imageinchange, (positionXY[4], positionXY[5]), 10, color, -1)

    color = listeCouleur[3]
    cv2.circle(imageinchange, (positionXY[6], positionXY[7]), 10, color, -1)

    cv2.line(imageinchange, (positionXY[0], positionXY[1]), (positionXY[2], positionXY[3]), (0, 0, 255), 3)
    cv2.line(imageinchange, (positionXY[2], positionXY[3]), (positionXY[6], positionXY[7]), (0, 0, 255), 3)
    cv2.line(imageinchange, (positionXY[6], positionXY[7]), (positionXY[4], positionXY[5]), (0, 0, 255), 3)
    cv2.line(imageinchange, (positionXY[4], positionXY[5]), (positionXY[0], positionXY[1]), (0, 0, 255), 3)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(imageinchange, 'XY1', (positionXY[0], positionXY[1]), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(imageinchange, 'XY2', (positionXY[2], positionXY[3]), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(imageinchange, 'XY3', (positionXY[4], positionXY[5]), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(imageinchange, 'XY4', (positionXY[6], positionXY[7]), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Test inchange", imageinchange)

create = True
# Create trackbar


def createTrackbar():
    global create

    cv2.createTrackbar('x1', 'Trackbar', pointsSouris[0][0], width, nothing)
    cv2.createTrackbar('y1', 'Trackbar', pointsSouris[0][1], height, nothing)

    cv2.createTrackbar('x2', 'Trackbar', pointsSouris[1][0], width, nothing)
    cv2.createTrackbar('y2', 'Trackbar', pointsSouris[1][1], height, nothing)

    cv2.createTrackbar('x3', 'Trackbar', pointsSouris[2][0], width, nothing)
    cv2.createTrackbar('y3', 'Trackbar', pointsSouris[2][1], height, nothing)

    cv2.createTrackbar('x4', 'Trackbar', pointsSouris[3][0], width, nothing)
    cv2.createTrackbar('y4', 'Trackbar', pointsSouris[3][1], height, nothing)
    create = False

def calcul():
    cv2.namedWindow("Trackbar")
    cv2.resizeWindow("Trackbar", 800, 500)
    cv2.moveWindow("Trackbar", 0, 10)
    cv2.namedWindow("Test inchange")
    cv2.moveWindow("Test inchange", 0, 10)
    cv2.setMouseCallback("Test inchange", click_and_crop)

    _, img = cam.read()
    cv2.imwrite("captureForBordsDetectopm.jpg", img)

    image = cv2.imread("captureForBordsDetectopm.jpg")

    global width
    global height
    height, width, channels = image.shape
    print height, width, channels




    while 1:

        if len(pointsSouris) == 4 and create == True:
            createTrackbar()

        key = cv2.waitKey(1) & 0xFF
        positionXY = []
        listeCouleur = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 255)]
        for i in range(4):
            for lettre in "xy":
                positionXY.append(cv2.getTrackbarPos(lettre + str(i + 1), 'Trackbar'))

        draw_circle(positionXY, listeCouleur)

        if key == ord("r"):
            cv2.destroyWindow("Trackbar")
            cv2.destroyWindow("Test inchange")
            print positionXY

            return positionXY

        if key == 27:
            cv2.destroyAllWindows()
            break

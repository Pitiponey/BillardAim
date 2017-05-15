import cv2
import numpy as np

class config():
    WIDTH = 50
    QUIT  = False

def pixel_color():
    while 1:
        img = cv2.imread("to_cut.jpg")


def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        pts1 = np.float32([[x - config.WIDTH, y - config.WIDTH],
                           [x + config.WIDTH, y - config.WIDTH],
                           [x - config.WIDTH, y + config.WIDTH],
                           [x + config.WIDTH, y + config.WIDTH]])
        pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

        M = cv2.getPerspectiveTransform(pts1, pts2)

        global dst
        dst = cv2.warpPerspective(pic, M, (300, 300))

        cv2.imshow("dst", dst)


    if event == cv2.EVENT_LBUTTONUP:
        cv2.imwrite("to_cut.jpg", dst)
        config.QUIT = True
        print "ecrit"


cv2.namedWindow("pic")
cv2.setMouseCallback('pic',draw_circle)
pic = cv2.imread("captureForBordsDetectopm.jpg")

while(1):
    cv2.imshow("pic", pic)
    if cv2.waitKey(20) & 0xFF == 27 or config.QUIT:
        break


cv2.destroyAllWindows()
pixel_color()
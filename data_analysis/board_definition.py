import cv2
import cv2.aruco as aruco
import numpy as np
from PIL import Image

'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''
#arucoType = aruco.DICT_6X6_100
#arucoType = aruco.DICT_6X6_1000 # The single marker
#arucoType = aruco.DICT_5X5_250


arucoType = aruco.DICT_4X4_250 # Markers on the side boundary

#arucoBoard = aruco.CharthuucoBoard_create(4,5,0.7,0.5,aruco.Dictionary_get(arucoType))
#arucoBoard = aruco.CharucoBoard_create(2,2,0.7,0.5,aruco.Dictionary_get(arucoType))
#arucoBoard = aruco.CharucoBoard_create(9,5,0.7,0.5,aruco.Dictionary_get(arucoType))
dictionary = cv2.aruco.getPredefinedDictionary(arucoType)

arucoBoard = aruco.CharucoBoard_create(9,5,0.7,0.5,aruco.Dictionary_get(arucoType))





board = arucoBoard.draw((7014,4962))



#for i in range(131,230):
#    singleMarker = aruco.drawMarker(aruco.Dictionary_get(arucoType),i,1200)
#    cv2.imwrite("/home/picard/markers/id" + str(i) + ".jpg", singleMarker)
#cv2.imwrite("/home/picard/markers/charucoCal.jpg",board)


from __future__ import print_function
import numpy as np
import cv2
import sys
import cv2.aruco as aruco
import rosbag
from cv_bridge import CvBridge, CvBridgeError

from board_definition import dictionary

bridge = CvBridge()
bag = rosbag.Bag('/home/picard/hddPlatte/caffe2_z2_color_direct_local_05Apr17_22h10m13s_Mr_Yellow/bair_car_2017-04-05-22-11-00_1.bag')

for topic, msg, t in bag.read_messages(topics=['/bair_car/zed/right/image_rect_color']):#, '/bair_car/encoder']):
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
#    cv2.imshow("Video",cv_image)
#    
#    if cv2.waitKey(1000/60) & 0xFF == ord('q'):
#        cv2.destroyAllWindows()
#        break

    aruco_dict = dictionary
    parameters =  aruco.DetectorParameters_create()

    res = aruco.detectMarkers(cv_image, aruco_dict, parameters=parameters)
    
    
    

    corners = res[0]
    ids = res[1]
    gray = cv_image
    if len(corners)>0:
        gray = aruco.drawDetectedMarkers(cv_image, corners)
        
        ''' c++ cv::aruco::estimatePoseCharucoBoard(charucoCorners, charucoIds, board, cameraMatrix, distCoeffs, rvec, tvec); 
        '''
        
        rvecOld = None
        tvecOld = None
        
        try:
            rvecOld = rvec
            tvecOld = tvec
        except:
            pass
            #rvec, tvec = aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeffs

        rvec, tvec = aruco.estimatePoseSingleMarkers(corners,0.20,cameraMatrix,distCoeffs)
        
        if rvecOld == None:
            rvecOld = rvec
            tvecOld = tvec
            
        drawPointAtSingleMarker(gray,rvec,tvec,rvecOld,tvecOld,cameraMatrix,distCoeffs)
       
          
    #other_format = cv2.cvtColor(gray,cv2.COLOR_BGR2RGB)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1000/30) & 0xFF == ord('q'):
        break
               

cv2.destroyAllWindows()
bag.close()

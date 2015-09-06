#! //anaconda/bin/python
from kzpy3.vis import *
import cv2
import sys
import numpy as np
import scipy.misc

haarPath = '/usr/local/Cellar/opencv/2.4.12/share/OpenCV/haarcascades'

if len(sys.argv) > 1:
    sleeptime = int(sys.argv[1])
else:
    sleeptime = 10
print(d2s('sleeptime =',sleeptime))

#face_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_frontalface_default.xml')#cascPath)
#eye_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_eye.xml')
#body_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_fullbody.xml')
video_capture = cv2.VideoCapture(0)
d = datetime.date.today()
path = opj(home_path,'scratch',str(d.year),str(d.today().month),str(d.today().day),'timelapse.'+str(np.int(np.floor(time.time()))))
print path
unix(d2s('mkdir -p',path))
ctr = 0
last_time = 0
while True:

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Video', np.fliplr(scipy.misc.imresize(frame,25)))

    if time.time()-last_time > sleeptime:
        last_time = time.time()
        fname = opj(path,d2p(np.int(np.floor(time.time())),'jpg'))
        print fname
        imsave(fname,rgbframe)
        ctr += 1

    time.sleep(0.2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

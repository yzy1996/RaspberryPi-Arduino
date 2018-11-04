from collections import deque
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

#下面定义颜色上下限，用的是hsv颜色而不是rgb颜色，自行百度！
# red1 = np.array([170, 100, 100])  
# red2 = np.array([179, 255, 255]) 
red1 = np.array([0, 0, 221])  
red2 = np.array([180, 30, 255]) 
mybuffer = 64  
pts = deque(maxlen=mybuffer)

#打开摄像头
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(1)

for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = image.array
	#颜色空间转换
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, red1, red2)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)	#找到物体轮廓，接受的参数是二值化的，参数（图像，只检测外轮廓，存储所有的轮廓点，相邻的两个点的像素位置差不超过1）
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  
    center = None  

    if len(cnts) > 0:	
        c = max(cnts, key = cv2.contourArea)  #contourArea是计算轮廓，找到
        ((x, y), radius) = cv2.minEnclosingCircle(c)  #找到外围圆
        M = cv2.moments(c)  
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))  #算出圆心

        if radius > 10:  
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) 
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    # for i in xrange(1, len(pts)):  
        # if pts[i - 1] is None or pts[i] is None:  
            # continue
        # thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
        # cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
		
    cv2.imshow("Frame", frame)   
    rawCapture.truncate(0)    # clear the stream in preparation for the next frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
	    break
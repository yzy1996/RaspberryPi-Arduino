from collections import deque
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import math
import time
import serial
import pygame

music_path = 'miao.mp3'
#获取的坐标值为（x,y）
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
radius = 0
sleeptime = 3  #定义的间隔时间
mode = 0  #定义是前进还是转向
flag = 0  #定义三次握手完成了吗
red1 = np.array([0, 0, 221])  
red2 = np.array([180, 30, 255]) 
mybuffer = 64  
pts = deque(maxlen=mybuffer)
direction = 0
pygame.mixer.init()
track=pygame.mixer.music.load("miao.mp3") #可以播放.mp3 .wav等多种格式的音频文件
#640*480
#判断点在视域的哪个范围
def judegeDir1(x, y):

	global direction1
	direction1 = 0
	#转向左边
	if x <= 280:
		direction1 = 1
	#转向右边
	if x >= 360:
		direction1 = 2
	return direction1
	
def judegeDir2(x, y):

	global direction2
	direction2 = 0	
	#前进
	if y <= 400:
		direction2 = 1
    #后退
	if y >= 260:
		direction2 = 2
		
	return direction2

try:
	while 1:
		if flag == 0:
			user1 = "hello"
			ser.write(user1.encode('utf-8'))
			response = ser.readline()
			print("connecting")
			user2 = "ack"
			if response.decode('utf-8') == "ack":
				ser.write(user2.encode('utf-8'))
				print("connecting ok!")
				flag = 1  
			
		
		if flag == 1:
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
					
				if center == None:
					x = 320
					y = 420
					user3 = 'x' + '\n'
					ser.write(user3.encode('utf-8'))
				else:
					
					pygame.mixer.music.play()
					x = int(center[0])
					y = int(center[1])
					
				print(x,end="")
				print('**',end="")
				print(y,end="")
				
				if radius > 10:  
					cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) 
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
					pts.appendleft(center)
			
				cv2.imshow("Frame", frame)   
				rawCapture.truncate(0)    # clear the stream in preparation for the next frame
					
				#计算距离
				distance = math.sqrt(pow((x - 320), 2) + pow((y - 420), 2))
				distance = int(distance)
				print("距离",end="")
				print(distance)
				

					
				#转向
				if mode == 0:	
					direction1 = judegeDir1(x ,y)	 				
					if direction1 == 1 :   #判断要向左转
						user = 'a' + '\n'
						print("向左")
						ser.write(user.encode('utf-8'))
					if direction1 == 2 :   #判断要向右转
						user = 'd' + '\n'   
						print("向右")
						ser.write(user.encode('utf-8'))
					if (direction1 == 0):
						mode = 1
					
				#直行
				if mode == 1:
					direction2 = judegeDir2(x ,y)	
					if direction2 == 1 :   #判断要向前走
						print("向前")
						user = 'w' + '\n'
						ser.write(user.encode('utf-8'))

					else:
						user = 'x' + '\n'
						print("停")
						ser.write(user.encode('utf-8'))
					mode = 0
				
				time.sleep(1)
				print(mode)
except KeyboardInterrupt:
    ser.close()
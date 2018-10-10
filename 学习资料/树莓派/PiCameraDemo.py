from picamera import PiCamera, Color
from time import sleep

demoCamera = PiCamera()

demoCamera.start_preview()    #打开摄像头预览
demoCamera.annotate_background = Color('white')
demoCamera.annotate_foreground = Color('red') 
demoCamera.resolution = (480, 320)      #设置摄像头的分辨率
demoCamera.framate = 60                 #设定摄像头的帧率
demoCamera.annotate_text = " SWS3009B - 2018"      #在图像上方显示一段文字
sleep(5)    #休息5秒
demoCamera.capture('/home/pi/Desktop/classPhoto.jpg')    #拍下一张照片
demoCamera.stop_preview()      #关闭摄像头预览
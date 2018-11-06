# coding:utf-8

# 加入摄像头模块，让小车实现自动循迹行驶

import RPi.GPIO as gpio
import time
import cv2
import numpy as np

# 定义引脚
in1 = 12
in2 = 16
in3 = 18
in4 = 22
center = 246.5
# 设置GPIO口为BOARD编号规范
gpio.setmode(gpio.BOARD)

# 设置GPIO口为输出
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)

# 设置PWM波,频率为500Hz
pwm1 = gpio.PWM(in1, 500)
pwm2 = gpio.PWM(in2, 500)
pwm3 = gpio.PWM(in3, 500)
pwm4 = gpio.PWM(in4, 500)
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)


# 定义向前
def go():
    pwm1.ChangeDutyCycle(50)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(50)
    pwm4.ChangeDutyCycle(0)


# 定义向右
def right():
    pwm1.ChangeDutyCycle(50)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(30)
    pwm4.ChangeDutyCycle(0)


# 定义向左
def left():
    pwm1.ChangeDutyCycle(30)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(50)
    pwm4.ChangeDutyCycle(0)


# 定义向后
def back():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(50)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(50)


# 定义停止
def stop():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(0)


cap = cv2.VideoCapture(0)
while (1):

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(gray.shape)
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # 膨胀，白区域变大
    dst = cv2.dilate(dst, None, iterations=2)
    # 腐蚀，白区域变小
    dst = cv2.erode(dst, None, iterations=6)

    # 单看第400行的像素值s
    color = dst[400]
    # 找到黑色的像素点个数s
    zero_count = np.sum(color == 0)
    zero_index = np.where(color == 0)

    # 找到黑色像素的中心点位置
    center = (zero_index[0][zero_count - 1] + zero_index[0][0]) / 2
    print(center)
    # # 定速行驶
    # # 当车走在中心上时，直行
    # if abs(center - 320) < 5:
    #     go()
    # # 当车需要右转
    # if center > 325:
    #     right()
    # # 当车需要左转
    # if center < 315 :
    #     left()

    # 变速行驶
    direction = center - 320

    if abs(direction) > 150:
        stop()

    # 要向右了，左轮要转快
    elif direction > 0:
        if direction > 70:
            direction = 70
        pwm1.ChangeDutyCycle(30 + direction)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(30)
        pwm4.ChangeDutyCycle(0)

    # 要向左了，右轮要转快
    elif direction < 0:
        if direction < -70:
            direction = -70
        pwm1.ChangeDutyCycle(30)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(30 - direction)
        pwm4.ChangeDutyCycle(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pwm1.stop()
pwm2.stop()
pwm3.stop()
pwm4.stop()
gpio.cleanup()

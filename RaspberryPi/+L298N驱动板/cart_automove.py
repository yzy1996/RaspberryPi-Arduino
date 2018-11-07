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



# 初始化定义
center = 320
# 打开摄像头
cap = cv2.VideoCapture(0)
while (1):
    ret, frame = cap.read()
    # 转化为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # 膨胀，白区域变大
    dst = cv2.dilate(dst, None, iterations=2)
    # # 腐蚀，白区域变小
    # dst = cv2.erode(dst, None, iterations=6)

    # 单看第400行的像素值s
    color = dst[400]
    # 找到黑色的像素点个数s
    zero_count = np.sum(color == 255)
    zero_index = np.where(color == 255)

    # 防止zero_count=0的报错
    if zero_count == 0:
        zero_count = 1

    # 找到黑色像素的中心点位置
    center = (zero_index[0][zero_count - 1] + zero_index[0][0]) / 2

    direction = center - 320
    # 变速行驶
    print(direction)
    # 停止
    if abs(direction) > 250:
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(0)

    # 直行
    elif abs(direction) < 20:
        pwm1.ChangeDutyCycle(100)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(100)
        pwm4.ChangeDutyCycle(0)

    # 右转
    elif direction > 20:
        # 限制在70以内
        if direction > 70:
            direction = 70
        pwm1.ChangeDutyCycle(30 + direction)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(30)
        pwm4.ChangeDutyCycle(0)

    # 左转
    elif direction < -20:
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

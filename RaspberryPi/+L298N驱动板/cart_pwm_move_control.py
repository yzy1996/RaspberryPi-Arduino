# coding:utf-8
import RPi.GPIO as gpio
import time, sys
from pynput import keyboard

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


# 定义向前
def go():
    pwm1.ChangeDutyCycle(50)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(50)
    pwm4.ChangeDutyCycle(0)
    # gpio.output(in1, gpio.HIGH)
    # gpio.output(in2, gpio.LOW)
    # gpio.output(in3, gpio.HIGH)
    # gpio.output(in4, gpio.LOW)


# 定义向右
def right():
    pwm1.ChangeDutyCycle(50)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(30)
    pwm4.ChangeDutyCycle(0)
    # gpio.output(in1, gpio.HIGH)
    # gpio.output(in2, gpio.LOW)
    # gpio.output(in3, gpio.LOW)
    # gpio.output(in4, gpio.HIGH)


# 定义向左
def left():
    pwm1.ChangeDutyCycle(30)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(50)
    pwm4.ChangeDutyCycle(0)
    # gpio.output(in1, gpio.LOW)
    # gpio.output(in2, gpio.HIGH)
    # gpio.output(in3, gpio.HIGH)
    # gpio.output(in4, gpio.LOW)


# 定义向后
def back():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(50)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(50)
    # gpio.output(in1, gpio.LOW)
    # gpio.output(in2, gpio.HIGH)
    # gpio.output(in3, gpio.LOW)
    # gpio.output(in4, gpio.HIGH)


# 定义停止
def stop():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(0)
    # gpio.output(in1, gpio.LOW)
    # gpio.output(in2, gpio.LOW)
    # gpio.output(in3, gpio.LOW)
    # gpio.output(in4, gpio.LOW)


def on_press(key):
    try:
        if key.char == 'w':
            go()
        if key.char == 'a':
            left()
        if key.char == 's':
            back()
        if key.char == 'd':
            right()
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    stop()
    if key == keyboard.Key.esc:
        return False


while True:
    with keyboard.Listener(
            on_press=on_press, on_release=on_release) as listener:
        listener.join()

# 秒级睡眠
#time.sleep(2)
pwm1.stop()
pwm2.stop()
pwm3.stop()
pwm4.stop()
gpio.cleanup()
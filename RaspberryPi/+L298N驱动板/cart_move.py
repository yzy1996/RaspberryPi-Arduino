# coding:utf-8
# 本代码实现 树莓派+L298N驱动板 小车的2s前进运动

import RPi.GPIO as gpio
import time

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

# 设置输出电平
gpio.output(in1, gpio.HIGH)
gpio.output(in2, gpio.LOW)
gpio.output(in3, gpio.HIGH)
gpio.output(in4, gpio.LOW)

# 秒级延迟
time.sleep(2)
# 释放
gpio.cleanup()
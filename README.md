# RaspberryPi-Arduino

目录下有三个主要文件夹[Arduino/Cat_classify/RaspberryPi]


## 树莓派

该文件夹是树莓派的程序，但搭配不同的下位机就有不同的实现方式，目前有两个子文件夹[+Arduino/+L298N]

### +L298N
首先要接好线
![接线方式](https://i.imgur.com/VQ4WiVQ.png)

cart_move.py：实现让小车向前行驶2秒。
cart_pwm_move_control.py：实现键盘控制小车前后左右，使用wasd操控，按下按键行驶，松开按键就会停止。

### +Arduino
首先也是接好线，参考学习资料

## Arduino

适用于树莓派加Arduino的硬件组合，树莓派提供上位机，Arduino提供下位机，

文件夹里是多个可以执行的代码，有些需要进行接线任务，请参考学习资料，代码的内容已经可以从名称中读出来。

最主要的是Remote_control的代码，这个是为了完成最终的任务，远程控制小车的行进，首先是建立三次握手，然后进行收发消息的控制，按WASD即可。


## Cat_classify

这是一个运用yolo3实现的识别猫图片的程序，模型已经训练好，可以直接使用，数据集可以到Mygithub dataset里面去下载。
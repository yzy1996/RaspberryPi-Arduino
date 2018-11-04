import pygame
pygame.mixer.init()
track=pygame.mixer.music.load("miao.mp3") #可以播放.mp3 .wav等多种格式的音频文件
pygame.mixer.music.play()


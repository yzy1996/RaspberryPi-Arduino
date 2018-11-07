import cv2
import numpy as np

img = cv2.imread('1.jpg')
print(img.shape)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
# 膨胀，白区域变大
dst = cv2.dilate(dst, None, iterations=2)	
# # 腐蚀，白区域变小
# dst = cv2.erode(dst, None, iterations=2)
cv2.imshow("capture", dst)
# 单看第400行的像素值s
color = dst[400]

# 找到黑色的像素点个数s
zero_count = np.sum(color == 255)

zero_index = np.where(color == 255)
# 找到黑色像素的中心点位置
center = (zero_index[0][zero_count-1] + zero_index[0][0]) / 2
print(center)
cv2.waitKey(0)
import cv2

cap = cv2.VideoCapture(0)

path = "photo/"
count = 0

while(1):
	
    ret, frame = cap.read()

    cv2.imshow("capture", frame)
	
    if cv2.waitKey(1) & 0xFF == ord('p'):
        cv2.imwrite(path + str(count) + ".jpg" , frame)
        count = count + 1
	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
		
cap.release()
cv2.destroyAllWindows()
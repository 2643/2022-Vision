import cv2 
import numpy as np

cap = cv2.VideoCapture(1)

lower_green = np.array([45,140,50]) 
upper_green = np.array([75,255,255])

lower_red = np.array([160,140,50]) 
upper_red = np.array([180,255,255])

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])



foundred = False

while(True):
    success,frame = cap.read()  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv,5)
    imgThreshHighred = cv2.inRange(hsv, lower_red, upper_red)
    imgThreshHighgreen = cv2.inRange(hsv, lower_green, upper_green)
    imgThreshHighblue = cv2.inRange(hsv, lower_blue, upper_blue)
    circlesred = cv2.HoughCircles(imgThreshHighred,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circlesblue = cv2.HoughCircles(imgThreshHighblue,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    circlesgreen = cv2.HoughCircles(imgThreshHighgreen,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    if circlesred is not None:
            print("found red")
#           print circlesred
    if circlesgreen is not None:
            print ("found green")
#           print circlesgreen
    if circlesblue is not None:
            print("found blue")
#           print circlesblue
    else:
            print("no ball") 

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
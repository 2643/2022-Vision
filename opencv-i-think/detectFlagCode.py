import cv2 as cv
import numpy as np
import math
import threading
import os
from concurrent.futures import ThreadPoolExecutor
# from networktables import NetworkTables

#capture = cv.VideoCapture(0)

# Connected_to_server = False

# cond = threading.Condition()
# notified = [False]
# def connect():
#     cond = threading.Condition()
#     notified = [False]

#     def connectionListener(connected, info):
#         print(info, '; Connected=%s' % connected)
#         with cond:
#             notified[0] = True
#             cond.notify()

#     NetworkTables.initialize(server='roborio-2643-frc.local')
#     NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

#     with cond:
#        print("Waiting")
#        if not notified[0]:
#            cond.wait()

#     return NetworkTables.getTable('vision-movement')


# if(Connected_to_server == False):
#     table = connect()
#     print("Connected!")


templates = [cv.imread('photos/68.jpg', 0), cv.imread('photos/68(2).jpg', 0), 
cv.imread('photos/74.5.jpg', 0), 
cv.imread('photos/84.jpg', 0), 
cv.imread('photos/68(3).jpg', 0), 
cv.imread('photos/115.jpg', 0), 
cv.imread('photos/162.jpg', 0), 
cv.imread('photos/209.jpg', 0), 
cv.imread('photos/256.jpg', 0), 
cv.imread('photos/303.jpg', 0)]

method = cv.TM_CCOEFF_NORMED

def calculation(P_y):
        if(P_y != 0):

            # realDistance = (focal*heightHub)/calibZeroPixels
            # # table.putNumber("Distance", realDistance)

            # degree = (math.atan(a/startingDistancePixels)*180)/math.pi
            # table.putNumber("Degree", degree)

            #degree2 = (math.atan(heightHub/realDistance))
            # table.putNumber("Degree2", degree2)

            # heightHub = 76.0
            # #Solution 1
            # startingInch = 105
            
            # startingDistancePixels = ((86*startingInch)/heightHub)
            # print(startingDistancePixels)

            # h3 = 76

            # angle1 = 55*math.pi/180

            # angle2 = (math.atan(startingDistancePixels/a2Pixels))

            # realDistance = h3/math.tan(angle1+angle2)

            #resolution_Y = 480

            resolution_Y = 1080
            angleCamera = 55*math.pi/180
            height = 76
            
            #FOV_vertical = 50.942
            FOV_vertical = 121.285*(math.pi/180)

            A_y = (P_y-(resolution_Y/2))/(resolution_Y/2)

            angleTwo = (A_y/2)*FOV_vertical

            realDistance = height/math.tan(angleCamera + angleTwo)
            #Solution 2
            # hubHeightPixels = middletoTop * (250/10)
            # DistanceinPixels = middletoTop * (240/10)

            # a3 = math.atan(hubHeightPixels/DistanceinPixels)
            # realDistance = h3/math.tan(a3)
            # a2 = a3-angle1

            # distance = h3/math.tan(a3)

            return (str(abs(realDistance)))
            '''+ " Degree: " + str(degree)'''
        else:
            return ("Robot too close/far to determine")



while True:

    #82 inches
    img = cv.imread("WIN_20221004_17_43_27_Pro.jpg")
    #111 Inches
    img = cv.imread("WIN_20221004_17_44_24_Pro.jpg")
	#150 inches
    img = cv.imread("WIN_20221004_17_45_27_Pro.jpg")
    #150
    #img = cv.imread("WIN_20221004_17_46_55_Pro.jpg")

    img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, img3 = cv.threshold(img2, 242, 255, 0)

    futures = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        for template in templates:
            future = executor.submit(cv.matchTemplate, img3, template, method)
            futures.append(future)
    while not all([i.done() for i in futures]):
        pass
    temp_res = [future.result() for future in futures]
    maxes = [np.amax(i) for i in temp_res]
    maximum = max(maxes)
    index = maxes.index(maximum)
    w, h = templates[index].shape[::-1]
    res = temp_res[index]

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if (maximum < 0.8) and (maximum > 0.42):
        cv.rectangle(img3,top_left, bottom_right, 255, 2)

        imgH, imgW = img3.shape

        rectTop = top_left[1]
        rectBottom = bottom_right[1]

        detectedHeightY = int((rectTop+rectBottom)/2)

        print(detectedHeightY)
        imageXisZero = int(imgW/2)
        imageYisZero = int(imgH/2)

        
        cv.line(img3, (imageXisZero, 0), (imageXisZero, imgH), color=255, thickness=3)
        cv.line(img3, (0, imageYisZero), (imgW, imageYisZero), color=255, thickness=2)

        cv.line(img, (0, imageYisZero), (imgW, imageYisZero), color=255, thickness=2)

        print("detected distance inches: ",  calculation(detectedHeightY))

    cv.imshow('img', img)
    cv.imshow('img3', img3)

    if cv.waitKey(1) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()
# importing libraries
import cv2 as cv
import numpy as np
   
# Create a VideoCapture object and read from input file
#cap = cv.VideoCapture('Ball-Vision\Videos\Ball\MovingAround.mp4')
cap = cv.VideoCapture(1)

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video  file")

i = 1
   
# Read until video is completed
while(cap.isOpened()):
      
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
   
    # Display the resulting frame
    cv.imshow('Frame', frame)
    key = cv.waitKey(200)
    # Press Q on keyboard to  exit
    if key == ord('q'):
      break
    elif key == ord('p'):
        cv.imwrite("Ball-Vision\Red\Photos\Halfway\Halfway ({}).jpg".format(i), frame)
        i = i + 1

   
  # Break the loop
  else: 
    break
   
# When everything done, release 
# the video capture object
cap.release()
   
# Closes all the frames
cv.destroyAllWindows()
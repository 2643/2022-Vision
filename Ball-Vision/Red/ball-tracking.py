import numpy as np
import cv2 as cv

#cap = cv.VideoCapture('Ball-Vision\Red\Videos\ShazWithBall.mp4')
cap = cv.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, captured_frame = cap.read()
    output_frame = captured_frame.copy()

    # Convert original image to HSV
    captured_frame_hsv = cv.cvtColor(captured_frame, cv.COLOR_BGR2HSV)

    # First blur to reduce noise prior to masking
    captured_frame_hsv = cv.medianBlur(captured_frame_hsv, 3)

    # Thresholding the  image to keep only the red pixels (far away)
    #captured_frame_hsv_red = cv.inRange(captured_frame_hsv, np.array([0, 117, 79]), np.array([5,176,233]))

    # Thresholding the  image to keep only the red pixels (close up)
    #captured_frame_hsv_red = cv.inRange(captured_frame_hsv, np.array([0, 86, 140]), np.array([6,175,256]))

    # Thresholding the  image to keep only the red pixels (halfway)
    #captured_frame_hsv_red = cv.inRange(captured_frame_hsv, np.array([0, 116, 102]), np.array([4,174,256]))

    # Thresholding the  image to keep only the red pixels (all distances)
    captured_frame_hsv_red = cv.inRange(captured_frame_hsv, np.array([0, 86, 79]), np.array([180,153,256]))

    # More blurs to reduce more noise, easier circle detection
    #captured_frame_hsv_red = cv.morphologyEx(captured_frame_hsv_red, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    captured_frame_hsv_red = cv.morphologyEx(captured_frame_hsv_red, cv.MORPH_CLOSE, np.ones((5,5),np.uint8))
    captured_frame_hsv_red = cv.GaussianBlur(captured_frame_hsv_red, (5, 5), 2, 2)
    
    # Use the Hough transform to detect circles in the image
    cv.imshow('hsv',captured_frame_hsv_red)
    circles = cv.HoughCircles(captured_frame_hsv_red, cv.HOUGH_GRADIENT_ALT, 1, captured_frame_hsv_red.shape[0] / 8, param1=300, param2=0.7, minRadius=11, maxRadius=300)

	# If we have extracted a circle, draw an outline
	# We only need to detect one circle here, since there will only be one reference object
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        #print(circles[0,2])
        cv.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)

    # Display the resulting frame, quit with q
    cv.imshow('frame', output_frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
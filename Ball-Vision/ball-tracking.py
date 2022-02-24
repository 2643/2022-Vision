import numpy as np
import cv2 as cv

cap = cv.VideoCapture('Ball-Vision\Videos\Ball\MovingAround.mp4')
#cap = cv.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, captured_frame = cap.read()
    output_frame = captured_frame.copy()

    # Convert original image to HSV
    captured_frame_hsv = cv.cvtColor(captured_frame, cv.COLOR_BGR2HSV)

    # First blur to reduce noise prior to masking
    captured_frame_hsv = cv.medianBlur(captured_frame_hsv, 3)

    # Thresholding the  image to keep only the blue pixels (far away)
    #captured_frame_hsv_blue = cv.inRange(captured_frame_hsv, np.array([109, 120, 55]), np.array([120,208,188]))

    # Thresholding the  image to keep only the blue pixels (close up)
    #captured_frame_hsv_blue = cv.inRange(captured_frame_hsv, np.array([102, 70, 58]), np.array([117,216,256]))

    # Thresholding the  image to keep only the blue pixels (halfway)
    #captured_frame_hsv_blue = cv.inRange(captured_frame_hsv, np.array([108, 100, 73]), np.array([118,218,252]))

    # Thresholding the  image to keep only the blue pixels (all distances)
    captured_frame_hsv_blue = cv.inRange(captured_frame_hsv, np.array([102, 70, 55]), np.array([117,208,256]))

    # More blurs to reduce more noise, easier circle detection
    captured_frame_hsv_blue = cv.morphologyEx(captured_frame_hsv_blue, cv.MORPH_OPEN, np.ones((5,5),np.uint8))
    #captured_frame_hsv_blue = cv.morphologyEx(captured_frame_hsv_blue, cv.MORPH_CLOSE, np.ones((5,5),np.uint8))
    captured_frame_hsv_blue = cv.GaussianBlur(captured_frame_hsv_blue, (5, 5), 2, 2)
    
    # Use the Hough transform to detect circles in the image
    cv.imshow('hsv',captured_frame_hsv_blue)
    circles = cv.HoughCircles(captured_frame_hsv_blue, cv.HOUGH_GRADIENT_ALT, 1, captured_frame_hsv_blue.shape[0] / 8, param1=300, param2=0.9, minRadius=10, maxRadius=300)

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
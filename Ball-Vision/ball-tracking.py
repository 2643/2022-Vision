import numpy as np
import cv2

cap = cv2.VideoCapture('Ball-Vision\Videos\Ball\VariousDist.mp4')
#cap = cv2.VideoCapture('Photos\WaterBottle.jpg')
#cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, captured_frame = cap.read()
    output_frame = captured_frame.copy()

    # Convert original image to BGR, since Lab is only available from BGR
    captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2HSV)

    # First blur to reduce noise prior to color space conversion
    captured_frame_lab = cv2.medianBlur(captured_frame_bgr, 3)

    # Thresholding the  image to keep only the blue pixels (far away)
    #captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([109, 120, 55]), np.array([120,193,162]))

    # Thresholding the  image to keep only the blue pixels (close up)
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([108, 112, 47]), np.array([120,214,209]))

    # More blurs to reduce more noise, easier circle detection
    captured_frame_lab_red = cv2.morphologyEx(captured_frame_lab_red, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    
    # Use the Hough transform to detect circles in the image
    cv2.imshow('hsv',captured_frame_lab_red)
    circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT_ALT, 1, captured_frame_lab_red.shape[0] / 8, param1=300, param2=0.9, minRadius=10, maxRadius=200)

	# If we have extracted a circle, draw an outline
	# We only need to detect one circle here, since there will only be one reference object
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        #print(circles[0,2])
        cv2.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)

    # Display the resulting frame, quit with q
    cv2.imshow('frame', output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
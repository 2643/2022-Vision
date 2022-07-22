# Python program to explain cv2.line() method 
   
# importing cv2 
import cv2
from cv2 import VideoCapture 

width = 240;
height = 320;

cap = VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width);
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height);

while(True):
    
    # Reading an image in grayscale mode
    ret, image = cap.read()
    
    # Window name in which image is displayed
    window_name = 'Image'
    
    # Start coordinate, here (225, 0)
    # represents the top right corner of image
    start_point = (image.shape[1], 0)
    
    # End coordinate, here (0, 225)
    # represents the bottom left corner of image
    end_point = (0, image.shape[0])
    
    # Black color in BGR
    color = (0, 0, 0)
    
    # Line thickness of 5 px
    thickness = 5
    
    # Using cv2.line() method
    # Draw a diagonal black line with thickness of 5 px
    image = cv2.line(image, start_point, end_point, color, thickness)
    
    # Displaying the image 
    cv2.imshow(window_name, image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
path.release()
cv2.destroyAllWindows() 
 
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([141,155,84])
    upper_blue = np.array([179, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    img_simulation = np.ones(mask.shape)
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    

    
    points = cv2.findNonZero(mask)
    print("points : ", points)
    #print("type est : ", type(points))
    if type(points) == np.ndarray:
        avg = np.mean(points, axis=0, dtype=np.int32) 
        print("avg : ", avg[0][0])
        print(mask.shape)
        x, y = avg[0][1], avg[0][0]
        center_coordinates = (avg[0][1], avg[0][0])


        # Radius of circle
        radius = 20
        # Line thickness of 2 px
        thickness = 2
        
        # Blue color in BGR
        color = (255, 0, 0)

        img_simulation = cv2.circle(img_simulation, center_coordinates, radius, color, thickness)
        cv2.imshow('img_simulation',img_simulation)

   
        
        
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
print("kmlna le while !")
print("les points fin sont : ",points )
cv2.destroyAllWindows()
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# define range of blue color in HSV (this is for the mask)
lower_blue = np.array([141,155,84])
upper_blue = np.array([179, 255, 255])
    
image = cv2.imread('white_image.jpeg') # it's gonna be use for the secondary interface
print(image.shape)
radius = 20  # radius of the circle
thickness = 15 # thickness of the circle


while(1):

    # Take each frame 
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    """      res = np.zeros(hsv.shape, hsv.dtype)
        w, h, z = hsv.shape
        for i in range(w) :
            for j in range(h):
                if hsv[i][j] not in mask[i]:
                    res[i][j] = 0
                else:
                    res[i][j] = 255"""
    #Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)


    # find the position of the red object   
    w, h, z = res.shape
    positions = []
    for i in range(w):
        for j in range(h):
            if mask[i][j] == 255:
                positions.append((i,j))
    
    # we calculate the mean of the positions
    somme_o=0
    somme_1=0

    for position in positions:

        somme_o += position[0]
        somme_1 += position[1]
    
    if len(positions)!=0:
        mean_position = (somme_o//len(positions),somme_1//len(positions))
    else: mean_position=(image.shape[0] // 2, image.shape[1] // 2)

    # we draw the circle in the secondary interface
    image = cv2.imread('white_image.jpeg')
    cv2.circle(image, (mean_position[0], image.shape[1] // 2), radius, (0, 0, 255), thickness = 15)
    cv2.imshow('image', image)
    cv2.waitKey(100)
        
    cv2.imshow('res',res)
    k = cv2.waitKey(15) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

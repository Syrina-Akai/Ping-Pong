import cv2
import numpy as np


img_simulation = np.ones((200,100))
center_coordinates = (20, 50)
# Radius of circle
radius = 20
# Line thickness of 2 px
thickness = 2

# Blue color in BGR
color = (255, 0, 0)

img_simulation = cv2.circle(img_simulation, center_coordinates, radius, color, thickness)
cv2.imshow('img_simulation',img_simulation)
cv2.waitKey(0)
cv2.destroyAllWindows()


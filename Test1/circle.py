import cv2
import numpy as np

image = cv2.imread('white_image.jpeg')
radius = 20
thickness = 15
x=0
y=400
while True:
    
    for i in range(np.random.randint(500), np.random.randint(500), 20):
        image = cv2.imread('white_image.jpeg')
        cv2.circle(image, (i, image.shape[1] // 2), radius, (0, 0, 255), thickness = 15)
        cv2.imshow('image', image)
        cv2.waitKey(100)
    
    


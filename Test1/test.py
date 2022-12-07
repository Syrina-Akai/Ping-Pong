import cv2
import numpy as np

lo = np.array([141,155,84])
hi = np.array([179, 255, 255])
radius = 20  # radius of the circle

def detect_inrange(image, surface):
    p = []
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.blur(image, (5, 5))
    mask = cv2.inRange(image, lo, hi)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    elems = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    elems = sorted(elems, key=lambda x:cv2.contourArea(x), reverse=True)
    for elem in elems:
        if cv2.contourArea(elem) > surface:
            ((x, y), _) = cv2.minEnclosingCircle(elem)
            p.append((int(x), int(y)))
        else:
            break
    return image, mask, p

videoCap = cv2.VideoCapture(0)
while(True):
    ret, frame = videoCap.read()
    cv2.flip(frame, 1, frame)
    image, mask, p = detect_inrange(frame, 200)
    
    #cv2.circle(image, (100, 100), 20, (0, 255, 0), 10)
    for i in p:
        print(i)
        cv2.circle(image, i, 10, (0, 255, 0), 10)
        #cv2.putText(image, str(i))
        #print(image[100, 100])
        font = cv2.FONT_HERSHEY_SIMPLEX
        # fontScale
        fontScale = 0.5
        # Blue color in BGR
        color = (255, 0, 0)
        # Line thickness of 2 px
        thickness = 2
        # Using cv2.putText() method
        image = cv2.putText(image, str(i), i, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow('image', image, )
    # we draw the circle in the secondary interface
    img = cv2.imread('Test1/white_image.jpeg')

    if p!=[]:
        cv2.circle(img, (p[0][0], img.shape[1] // 2), radius, (0, 0, 255), thickness = 15)
        cv2.imshow('img', img)
        cv2.waitKey(100)
    else:
        cv2.imshow('img', img)
        cv2.waitKey(100)

    if mask is not None:
        cv2.imshow('mask', mask)
    if cv2.waitKey(10)&0xFF == ord('0') :
        break

videoCap.release()
cv2.destroyAllWindows()
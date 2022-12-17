import cv2
import numpy as np
from KalmanFilter import KalmanFilter

lo = np.array([100, 100, 100])
hi = np.array([130, 255, 255])
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

def detect_visage(image):
    face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")
    points=[]
    rects=[]
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)
    for x, y, w, h in face:
        points.append(np.array([int(x+w/2), int(y+h/2)]))
        rects.append(np.array([(x,y), (x+w, y+h)]))
    return points, rects


VideoCap = cv2.VideoCapture(0)
KF = KalmanFilter(0.1, [10, 10])
rects = None
while(True):
    ret, frame = VideoCap.read()
    cv2.flip(frame, 1, frame)
    #points, rects = detect_visage(frame)
    image, mask, points = detect_inrange(frame, 300)
    etat =  KF.predict().astype(np.int32)
    cv2.circle(frame, (int(etat[0]), int(etat[1])), 2, (0,255,0), 5)
    cv2.arrowedLine(frame, (int(etat[0]), int(etat[1])), 
                            (int(etat[0]+etat[2]),int(etat[1]+etat[3])), 
                            color=(0,255,0),
                            thickness=3,
                            tipLength=0.2)
    if len(points)>0 :
        KF.update(np.expand_dims(points[0], axis=-1))
        cv2.circle(frame, (points[0][0], points[0][1]), 10, (0,0,255), 2)
    if rects is not None :
        try : 
            for rect in rects:
                cv2.rectangle(frame, rect[0],rect[1], (0,0,255),1,cv2.LINE_AA )
        except:
            print("erreur")
    cv2.imshow('image', frame)
    if cv2.waitKey(10)&0xFF == ord('q'):
        break
VideoCap.release()
cv2.destroyAllWindows()
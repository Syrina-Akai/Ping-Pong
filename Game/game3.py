import cv2
import numpy as np
from racket import Racket 
from ball import Ball

class BriksGame:
    def __init__(self, h=600, w=810, game_speed=50, color="blue"):
        
        self.game_speed = game_speed
        self.h = 600
        self.w = 810
        self.cell_h = 30
        self.cell_w = 150
        #colors
        self.grid_color = (1., 1., 1.)
        self.racket_color = (0.7, 0.3, 0.7)  
        self.ball_color = (0., 0.2, 0.8)
        self.brik_color = [ (0.8, 0.4, 0.5),(0.8, 0.5, 0.3), (0.8, 0.5, 0.4 ), (0.9, 0.5, 0.5), 
                            (0.9, 0.6, 0.7 ), (0.8, 0.6, 0.5), (1., 0.7, 0.6)]
        #creation de l'image
        self.img = np.ones((h, w, 3))*self.grid_color
        #create racket
        self.racket = Racket(self.img, self.h, self.w)
        #create ball
        self.ball = Ball(self.img, self.h, self.w)
        #game over
        self.game_over = False
        if color == "red":
            self.lo = np.array([141,155,84])
            self.hi = np.array([179, 255, 255])
        elif color == "green":
            self.lo = np.array([40, 100, 100])
            self.hi = np.array([70, 255, 255])
        elif color == "blue":
            self.lo = np.array([100, 100, 100])
            self.hi = np.array([130, 255, 255])

    # Detects the color of the object in the frame
    def detect_inrange(self, image, surface):

        p = []
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # convert to HSV
        image = cv2.blur(image, (5, 5)) # blur the image to reduce noise
        mask = cv2.inRange(image, self.lo, self.hi) # create a mask to detect the color
        mask = cv2.erode(mask, None, iterations=2) # remove noise 
        mask = cv2.dilate(mask, None, iterations=2) # remove noise
        elems = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] # find contour to detect the object
        elems = sorted(elems, key=lambda x:cv2.contourArea(x), reverse=True) # sort contours to
        for elem in elems:
            # if the contour is big enough, draw it on the frame
            if cv2.contourArea(elem) > surface:
                ((x, y), _) = cv2.minEnclosingCircle(elem)
                p.append((int(x), int(y)))
            else:
                break
        return image, mask, p


    #le jeu !
    def play(self):
        radius = 20  # radius of the circle
        # For webcam input:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            self.__init__()
            while not self.ball.game_over :
                cv2.imshow('Break briks', self.img)
                self.ball.move_ball()
                ret, frame = cap.read()
                if not ret:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue
                cv2.flip(frame, 1, frame)
                image, mask, p = self.detect_inrange(frame, 200)
                # we draw the circle in the secondary interface
                img = cv2.imread('Game/white_image.jpeg')
                if p!=[]:
                    cv2.circle(img, (p[0][0], p[0][1]), radius, (0, 0, 255), thickness = 15)
                    cv2.imshow('img', img)
                    cv2.waitKey(5)
                    self.racket.move_racket_with_camera(abs(int(p[0][0])), abs(int(p[0][1])))
                else:
                    cv2.imshow('img', img)
                    cv2.waitKey(5)

                if cv2.waitKey(10)&0xFF == ord('0') :
                    break

            choice = ''
            while choice not in ['y', 'n']:
                cv2.imshow('Break briks', self.img)
                choice = chr(cv2.waitKey(0) & 0xFF)
            if choice == 'n':
                break
        cap.release()
        cv2.destroyAllWindows()
        
#let's play ! ^^
briksGame = BriksGame()
briksGame.play()

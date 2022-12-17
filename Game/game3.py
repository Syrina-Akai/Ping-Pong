import cv2
import numpy as np
from racket import Racket 
from ball import Ball

class BriksGame:
    def __init__(self, h=600, w=810, game_speed=50, color="red"):
        
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
        #detected color
        self.colors = ['blue', 'green', 'red']

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
    
    def getColor(self, color):
        self.color = [idx for idx in self.colors if idx[0].lower() == color.lower()]
        self.color=self.color[0]
        if self.color == "red":
            self.lo = np.array([141,155,84])
            self.hi = np.array([179, 255, 255])
            self.circle_color = (0, 0, 255)
        elif self.color == "green":
            self.lo = np.array([40, 100, 100])
            self.hi = np.array([70, 255, 255])
            self.circle_color = (0,128,0)
        elif self.color == "blue":
            self.lo = np.array([100, 100, 100])
            self.hi = np.array([130, 255, 255])
            self.circle_color = (255,0,0)

    def choose_color(self):
        self.img[self.h//5:self.h*4//6, self.w//5:self.w*4//5] = (0.2, 0.2, 0.2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.img, "Welcome to bricks breaker !", (self.w//4, self.h*2//7), font, 0.9, (1., 1., 1.), 2, 2)
        cv2.putText(self.img, "Choose the detected color : ", (self.w//3, (self.h*2//7)+60), font, 0.75, (1., 1., 1.), 1, 2)
        cv2.putText(self.img, "Press 'b' to play with blue color", (self.w//3, (self.h*4//10)+30), font, 0.5, (1., 1., 1.), 1, 2)
        cv2.putText(self.img, "Press 'g' to play with green color", (self.w//3, (self.h*4//10)+60), font, 0.5, (1., 1., 1.), 1, 2)
        cv2.putText(self.img, "Press 'r' to play with red color", (self.w//3, (self.h*4//10)+90), font, 0.5, (1., 1., 1.), 1, 2)


    #le jeu !
    #fontion pour afficher le menu
    def play_color(self):
        self.__init__()
        radius = 20  # radius of the circle
        # For webcam input:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            while not self.ball.game_over :
                cv2.imshow('Bricks Breaker', self.img)
                self.ball.move_ball()
                ret, frame = cap.read()
                if not ret:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue
                cv2.flip(frame, 1, frame)
                image, mask, p = self.detect_inrange(frame, 200)
                # we draw the circle in the secondary interface
                img = np.ones((image.shape))
                if p!=[]:
                    cv2.circle(img, (p[0][0], p[0][1]), radius, self.circle_color, thickness = 15)
                    cv2.imshow("Color's position", img)
                    cv2.waitKey(5)
                    self.racket.move_racket_with_camera(abs(int(p[0][0])), abs(int(p[0][1])))
                else:
                    cv2.imshow("Color's position", img)
                    cv2.waitKey(5)
                if cv2.waitKey(10)&0xFF == ord('0') :
                    break
            if self.ball.game_over:
                cv2.destroyWindow("Color's position")
                break
        choice = ''
        while choice not in ['y', 'n']:
            cv2.imshow('Bricks Breaker', self.img)
            choice = chr(cv2.waitKey(0) & 0xFF)
        if choice == 'n':
            self.break_game = True
    
    def play_game(self):#game with menu
        self.break_game = False
        while not self.break_game:
            cap = cv2.VideoCapture(0)
            while cap.isOpened():
                self.__init__()
                self.choose_color()
                color = ''
                while color.lower() not in ['b', 'g', 'r'] :
                    cv2.imshow('Bricks Breaker', self.img)
                    color = chr(cv2.waitKey(0) & 0xFF)
                color = color.lower()
                #get the low and hight intervall of the color
                self.getColor(color)
                self.play_color()
        cv2.destroyAllWindows()

    #game without menu
    def play(self):
        radius = 20  # radius of the circle
        # For webcam input:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            self.__init__()
            while not self.ball.game_over :
                cv2.imshow('Bricks Breaker', self.img)
                self.ball.move_ball()
                ret, frame = cap.read()
                if not ret:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue
                cv2.flip(frame, 1, frame)
                image, mask, p = self.detect_inrange(frame, 200)
                
                # we draw the circle in the secondary interface
                img = np.ones((image.shape))
                if p!=[]:
                    cv2.circle(img, (p[0][0], p[0][1]), radius, (0, 0, 255), thickness = 15)
                    cv2.imshow("Color's position", img)
                    cv2.waitKey(5)
                    self.racket.move_racket_with_camera(abs(int(p[0][0])), abs(int(p[0][1])))
                else:
                    cv2.imshow("Color's position", img)
                    cv2.waitKey(5)

                if cv2.waitKey(10)&0xFF == ord('0') :
                    break

            choice = ''
            while choice not in ['y', 'n']:
                cv2.imshow('Bricks Breaker', self.img)
                choice = chr(cv2.waitKey(0) & 0xFF)
            if choice == 'n':
                break
        cap.release()
        cv2.destroyAllWindows()
        
#let's play ! ^^
briksGame = BriksGame()
briksGame.play_game()

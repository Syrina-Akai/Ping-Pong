import cv2
import numpy as np
from racket import Racket 
from ball import Ball
import mediapipe as mp

class BriksGame:
    def __init__(self, h=600, w=810, game_speed=50):
        
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

        self.game_over = False
    
    #le jeu ! 
    def play(self):
        mp_hands = mp.solutions.hands
        radius = 20  # radius of the circle
        # For webcam input:
        cap = cv2.VideoCapture(0)

        with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                self.__init__()
                while not self.ball.game_over :
                    cv2.imshow('Break briks', self.img)
                    self.ball.move_ball()
                    success, image = cap.read()
                    if not success:
                        print("Ignoring empty camera frame.")
                        # If loading a video, use 'break' instead of 'continue'.
                        continue

                    # Flip the image horizontally for a later selfie-view display, and convert
                    # the BGR image to RGB.
                    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                    # To improve performance, optionally mark the image as not writeable to
                    # pass by reference.
                    image.flags.writeable = False
                    results = hands.process(image)
                    image_height, image_width, _ = image.shape    # Draw the hand annotations on the image.
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Here is How to Get All the Coordinates
                            cx, cy = hand_landmarks.landmark[10].x * image_width, hand_landmarks.landmark[10].y*image_height

                            cv2.circle(image, (abs(int(cx)), abs(int(cy))), 10, (0, 255, 0), 10)
                            # we draw the circle in the secondary interface
                            img = cv2.imread('Game/white_image.jpeg')
                            cv2.circle(img, (abs(int(cx)), img.shape[1] // 2), radius, (0, 0, 255), thickness = 15)
                            cv2.imshow('img', img)
                            cv2.waitKey(5)
                            self.racket.move_racket_with_camera(abs(int(cx)), abs(int(cy)))
                    cv2.imshow('MediaPipe Hands', image)
                    if cv2.waitKey(5) & 0xFF == 27:
                        break
                choice = ''
                while choice not in ['y', 'n']:
                    cv2.imshow('Break briks', self.img)
                    choice = chr(cv2.waitKey(0) & 0xFF)
                if choice == 'n':
                    break
            cv2.destroyAllWindows()
        cap.release()
        
#let's play ! ^^
briksGame = BriksGame()
briksGame.play()

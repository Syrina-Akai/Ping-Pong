import platform
import cv2
import numpy as np
from racket import Racket 
from ball import Ball
import random

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
        if platform.system() == 'Windows':
            UP_KEY, LEFT_KEY, DOWN_KEY, RIGHT_KEY = 2490368, 2424832, 2621440, 2555904
        elif platform.system() == 'Linux':
            UP_KEY, LEFT_KEY, DOWN_KEY, RIGHT_KEY = 65362, 65361, 65364, 65363
        while(1):
            self.__init__()
            while not self.ball.game_over :
                cv2.imshow('Break briks', self.img)
                self.ball.move_ball()
                
                k = cv2.waitKeyEx(self.game_speed)
                self.racket.direction = ''
                if k == UP_KEY :
                    self.racket.direction = 'up'
                elif k == LEFT_KEY :
                    self.racket.direction = 'left'
                elif k == DOWN_KEY :
                    self.racket.direction = 'down'
                elif k == RIGHT_KEY :
                    self.racket.direction = 'right'
                if self.racket.direction != '':
                    self.racket.move_racket()
            choice = ''
            while choice not in ['y', 'n']:
                cv2.imshow('Break briks', self.img)
                choice = chr(cv2.waitKey(0) & 0xFF)
            if choice == 'n':
                break
        cv2.destroyAllWindows()


#let's play ! ^^
briksGame = BriksGame()
briksGame.play()
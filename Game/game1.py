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

    def draw_ball(self, pos, color):
        cv2.circle(self.img, pos, 2, color, self.r)

    def move_ball(self):
        delta = self.move_map[self.direction]
        new_y, new_x = self.ball[0]+delta[0], self.ball[1]+delta[1]
        print("*************y : ",new_y," x : ", new_x,"*************")
        #cela veut dire que la balle est en milieux  : 
        if new_y < self.h and new_y>0 and new_x>0 and new_x < self.h:
            print("y : ",new_y," x : ", new_x)
            print( self.img[new_y, new_x])

            #la balle est en bas :
            if new_x+self.r//2 < self.h and new_y <self.h : 
                print("y : ",new_y," x : ", new_x+self.r//2)
                #si la balle a touche la raquette
                if (self.img[new_x+self.r//2, new_y] == self.racket_color).all() :
                    print("***on a touche la raquette***")
                    self.direction = random.choice(self.move_up)
                #si la balle est en haut
                elif new_x <= self.r :
                    print("we're going down y : ",new_y," x : ", new_x)
                    self.direction = random.choice(self.move_down)
        
        #game over
        elif new_x>=self.h:
            print("end game...")
            self.end_game()
        #si la balle est à gauche => y <0
        elif new_y-2*np.sqrt(self.r) <=np.sqrt(self.r) :
            self.direction = random.choice(self.move_right)
        #si la balle est à droite
        elif new_y >self.w- self.r*2:
            print("we're going right : ", new_x)
            self.direction = random.choice(self.move_left)
        #les failles => cas specials
        elif new_y >= self.h :
            if new_x <= self.r :
                print("we're going down y : ",new_y," x : ", new_x)
                self.direction = random.choice(self.move_down)
            elif new_x+self.r//2 < self.w : 
                if (self.img[new_x+self.r//2, new_y] == self.racket_color).all() :
                    print("***on a touche la raquette***")
                    self.direction = random.choice(self.move_up)
            
        delta = self.move_map[self.direction]
        new_y, new_x = self.ball[0]+delta[0], self.ball[1]+delta[1]
        self.draw_ball(self.ball, self.grid_color)
        self.ball = (new_y, new_x)
        self.draw_ball(self.ball, self.ball_color)

    def end_game(self):
        self.game_over = True
        self.img[self.h//5:self.h*4//6, self.w//5:self.w*4//5] = (0.2, 0.2, 0.2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.img, 'Game over!', (self.w//3, self.h*2//7), font, 1.5, (1., 1., 1.), 4, 2)
        cv2.putText(self.img, 'Press y to play again or n to quit', (self.w//4, self.h * 5 // 8), font, 0.75, (1., 1., 1.), 1, 2)
        
    #le jeu !
    def play(self):
        if platform.system() == 'Windows':
            UP_KEY, LEFT_KEY, DOWN_KEY, RIGHT_KEY = 2490368, 2424832, 2621440, 2555904
        elif platform.system() == 'Linux':
            UP_KEY, LEFT_KEY, DOWN_KEY, RIGHT_KEY = 65362, 65361, 65364, 65363
        while(1):
            self.__init__()
            while not self.game_over :
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
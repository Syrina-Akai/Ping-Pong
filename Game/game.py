import cv2
import numpy as np
from collections import defaultdict
from racket import Racket 
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
        self.r = 20
        self.initial_position = ((self.h-self.r)//2, (self.w-self.r)//2)
        self.ball = ((self.h-self.r)//2, (self.w-self.r)//2)
        self.draw_ball(self.ball, self.ball_color)

        self.move_map = defaultdict(lambda: (0, 0))
        self.move_map.update({
            'up-right' : (self.r//2, -self.r//2),
            'up-left' : (-self.r//2, -self.r//2),
            'down-right' : (self.r//2, self.r//2),
            'down-left' : (-self.r//2, self.r//2)
        })
        self.direction = 'up-right'
        self.move_up = ['up-right', 'up-left']
        self.move_down = ['down-right', 'down-left']

        self.game_over = False

    def draw_ball(self, pos, color):
        cv2.circle(self.img, pos, 2, color, self.r)

    def move_ball(self):
        delta = self.move_map[self.direction]
        new_y, new_x = self.ball[0]+delta[0], self.ball[1]+delta[1]

        
        if new_y < self.h and new_x < self.w:
            print("y : ",new_y," x : ", new_x)
            print( self.img[new_y, new_x])
            
            if new_y+self.r*2+1 < self.h or new_y+self.r*2+1 < self.w:
                print("y : ",new_y+self.r*2+1," x : ", new_x, " color => ", self.img[new_x, new_y+self.r*2+1])
                if (self.img[new_x, new_y+self.r*2+1] == self.racket_color).all() or (self.img[new_x, new_y-(self.r*2+1)] == self.racket_color).all():
                    print("9asseha!!!!!!!")
                    self.direction = random.choice(self.move_up)
                    
                elif new_y >=(self.h - np.sqrt(self.r)) or new_y <=0 or new_x >=(self.w-np.sqrt(self.r)) or new_x <=0:
                    #on ajoute ici la suppression des briques !
                    print("************************************************************************")
                    print("we're going down y : ",new_y," x : ", new_x)
                    self.direction = random.choice(self.move_down)
            
        elif new_y >= self.h : 
            print("new_y >= self.h", new_y)
            self.direction = random.choice(self.move_down) 
        elif new_y <=0 : 
            print("new_y <=0")
            self.direction = random.choice(self.move_up)
        elif new_x >= self.w or new_x <=0:
            self.direction = random.choice([self.move_map.values])
        elif new_y+self.r*2 >= self.w : 
            self.end_game()
            
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
        UP_KEY, LEFT_KEY, DOWN_KEY, RIGHT_KEY = 2490368, 2424832, 2621440, 2555904
        while(1):
            self.__init__()
            while not self.game_over :
                cv2.imshow('Break briks', self.img)
                self.move_ball()
                
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
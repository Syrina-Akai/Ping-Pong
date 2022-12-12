import cv2
import numpy as np
from collections import defaultdict
import random

class Ball:
    def __init__(self, img, h=600, w=810):
        self.h = h
        self.w = w
        self.img = img
        self.r = 20
        self.ball_color = (0., 0.2, 0.8)
        self.racket_color = (0.7, 0.3, 0.7)
        self.grid_color = (1., 1., 1.)

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
        self.direction = 'down-right'
        self.move_up = ['up-right', 'up-left']
        self.move_down = ['down-right', 'down-left']
        self.move_right = ['up-right', 'down-right']
        self.move_left = ['up-left', 'down-left']
        self.game_over=False
        self.score = 0

    def draw_ball(self, pos, color):
        cv2.circle(self.img, pos, 2, color, self.r)

    def move_ball(self):
        delta = self.move_map[self.direction]
        new_y, new_x = self.ball[0]+delta[0], self.ball[1]+delta[1]
        #cela veut dire que la balle est en milieux  : 
        if new_y < self.h and new_y>0 and new_x>0 and new_x < self.h:

            #la balle est en bas :
            if new_x+self.r//2 < self.h and new_y <self.h : 
                #si la balle a touche la raquette
                if (self.img[new_x+self.r//2, new_y] == self.racket_color).all() :
                    self.direction = random.choice(self.move_up)
                    self.score+=1
                #si la balle est en haut
                elif new_x <= self.r :
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
            self.direction = random.choice(self.move_left)

        #les failles => cas specials
        elif new_y >= self.h :
            if new_x <= self.r :
                #print("we're going down y : ",new_y," x : ", new_x)
                self.direction = random.choice(self.move_down)
            elif new_x+self.r//2 < self.h : 
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
        cv2.putText(self.img, 'Score:', (self.w*7//16, self.h * 3 // 8), font, 1.1, (1., 1., 1.), 1, 2)
        cv2.putText(self.img, str(self.score), (self.w * 7// 15, self.h * 4//8), font, 2, (1., 1., 1.), 3, 2)
        cv2.putText(self.img, 'Press y to play again or n to quit', (self.w//4, self.h * 5 // 8), font, 0.75, (1., 1., 1.), 1, 2)
        self.score=0
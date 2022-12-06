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
        self.ball_position = ((self.h-self.r)//2, (self.w-self.r)//2) 
        self.draw_ball(self.ball_position)
        self.move_map = defaultdict(lambda: (0, 0))
        self.move_map.update({
            'up-right' : (-self.r, self.r),
            'up-left' : (self.r, -self.r),
            'down-right' : (self.r, self.r),
            'down-left' : (self.r, -self.r)
        })
        self.direction = 'down-right'
        self.move_up = ['up-right', 'up-left']
        self.move_down = ['down-right', 'down-left']

    def draw_ball(self, pos):
        cv2.circle(self.img, pos, 2, self.ball_color, self.r)

    def move_ball(self):
        delta = self.move_map[self.direction]
        new_y, new_x = self.ball_position[0]+delta[0], self.ball_position[1]+delta[1]
        
        if (self.img[new_y, new_x] == self.racket_color).all():
            self.direction = random.choice(self.move_up)
            delta = self.move_map[self.direction]
            new_y, new_x = self.ball_position[0]+delta[0], self.ball_position[1]+delta[1]
            
        elif new_y >=(self.h - self.r) and new_y <=self.r and  new_x >=self.w-self.r*9//10 and new_x <0:
            #on ajoute ici la suppression des briques !
            self.direction = random.choice(self.move_down)
            delta = self.move_map[self.direction]
            new_y, new_x = self.ball_position[0]+delta[0], self.ball_position[1]+delta[1]
            
        self.draw_ball((new_y, new_x))

        


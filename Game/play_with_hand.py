import cv2
import numpy as np
from collections import defaultdict

class Racket:
    def __init__(self, img, h=600, w=810):
        self.h = h
        self.w = w
        
        self.img = img
        self.cell_h = 30
        self.cell_w = 150
        self.racket_color = (0.7, 0.3, 0.7)
        self.grid_color = (1., 1., 1.)
        #position initial de la raquette
        self.initial_pos = (self.h-self.cell_h*2, (self.w-self.cell_w)//2)
        self.racket = self.initial_pos
    
        #creation de la raquette 
        self.color_square(self.racket, self.racket_color)
        
        print("y = ", self.initial_pos[0],"-",self.initial_pos[0]+self.cell_h, "x = ", self.initial_pos[1], "-", self.initial_pos[1]+self.cell_w ,self.img[self.initial_pos])
        """    #map pour sauvegarder les mouvements
            self.move_map = defaultdict(lambda: (0, 0))
            self.move_map.update({
                'left': (0, -self.cell_h),
                'right': (0, self.cell_h),
                'up': (-self.cell_h, 0),
                'down': (self.cell_h, 0)
            })
            self.direction = ''"""

    #ceci est principalement pour colorier une matrice à partir de sa position
    def color_square(self, pos, color):
        y, x = pos
        self.img[y:y+self.cell_h, x:x+self.cell_w] = color
        self.racket_position = {'y':[y, y+self.cell_h], 'x': [x,x+self.cell_w]}
    
    """    #movement => ça bouge pas verticalement pour le moment
        def move_racket(self):
            delta = self.move_map[self.direction]
            new_y, new_x = self.racket[0]+delta[0], self.racket[1]+delta[1]

            if new_y <(self.h - self.cell_h) and new_y >self.cell_h and  new_x <self.w-self.cell_w*9//10 and new_x >=0:
                self.color_square(self.racket, self.grid_color)
                self.color_square((self.racket[0], new_x), self.racket_color)
                self.racket = (self.racket[0], new_x)
            self.direction = ''"""

    def move_racket_with_hand(self, x, y):
        new_y, new_x = self.racket[0]+y, self.racket[1]+x
        if new_y <(self.h - self.cell_h) and new_y >self.cell_h and  new_x <self.w-self.cell_w*9//10 and new_x >=0:
            self.color_square(self.racket, self.grid_color)
            self.color_square((self.racket[0], new_x), self.racket_color)
            self.racket = (self.racket[0], new_x)
        


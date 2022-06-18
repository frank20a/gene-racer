import pygame as pg
import numpy as np

class LidarsSprite(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.image = parent.screen
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        
    def update(self):
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        car = sorted(self.parent.cars)[0]
        for l, r in zip(car.lidars, car.measurement):
            l = 180 * l / np.pi + car.a
            self.rect.union(pg.draw.line(self.parent.screen, (3, 152, 252), (car.x, car.y), (r * np.cos(l) + car.x, r * np.sin(l) + car.y)))
            
        self.rect = self.image.get_rect()
    
        
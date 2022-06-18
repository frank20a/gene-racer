import pygame as pg

class ScoreText(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        
    def update(self):
        car = sorted(self.parent.cars)[-1]
        self.image = self.parent.font1.render(f'Best: {car.name} - {car.score:.1f}', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 30)
        
    
class EpochText(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        
    def update(self):
        self.image = self.parent.font1.render(f'Epoch: {self.parent.epoch}', True,  (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (300, 30)
    
    def draw(self):
        pass


class BestScoreText(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        
    def update(self):
        self.image = self.parent.font1.render(f'Last Best: {self.parent.prev_best[0]} - {self.parent.prev_best[1]:.1f}', True,  (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (450, 30)
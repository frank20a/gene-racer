import pygame as pg

class ScoreText(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        
    def update(self):
        self.image = self.parent.arial20.render(f"Score: {sorted(self.parent.cars)[-1].score:.1f}", True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (15, 15)
    
    def draw(self):
        pass
        
    
class EpochText(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        
    def update(self):
        self.image = self.parent.arial20.render(f"Epoch: {self.parent.epoch}", True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (115, 15)
    
    def draw(self):
        pass
        
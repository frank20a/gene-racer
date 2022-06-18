import pygame as pg
from scripts import ComputerCar, PlayerCar, Track
from scripts.text import ScoreText
import numpy as np
from scripts.lidar import LidarsSprite

class Engine:
    pg.font.init()
    arial20 = pg.font.SysFont("arial", 20)
    
    def __init__(self, level: str, n_cars: int = 1, player: str = 'player'):
        super().__init__()
        pg.init()
        
        # Setters
        self.track = Track(level)
        self.w, self.h = self.track.w, self.track.h
        self.player = player
        pg.display.set_caption(f"Gene Racer - {self.track.name}")
        # self.logo = pg.image.load(os.path.join(os.environ['GAME_DIR'], f'engine\images\logo32x32.png'))
        # pg.display.set_icon(self.logo)
        self.screen = pg.display.set_mode((self.w, self.h))
        self.running = False
        self.background = pg.Surface(self.screen.get_size())
        self.background.blit(self.track.texture.convert(), (0, 0))
        self.screen.blit(self.background, (0, 0))
        self.clock = pg.time.Clock()
        
        if self.player == 'player':
            self.cars = [PlayerCar(self) for _ in range(n_cars)]
        elif self.player == 'computer':
            self.cars = [ComputerCar(self) for _ in range(n_cars)]
            self.epoch = 0
        
        # Sprites
        self.sprites = pg.sprite.RenderUpdates(self.cars)
        ScoreText(self).add(self.sprites)
    
    def mainloop(self):
        self.running = True
        pg.display.flip()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        
        self.cleanup()
            
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        if self.player == 'player':
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]  and not keys[pg.K_RIGHT]:   self.cars[0].left()
            if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:    self.cars[0].right()
            if keys[pg.K_UP]    and not keys[pg.K_DOWN]:    self.cars[0].forward()
            if keys[pg.K_DOWN]  and not keys[pg.K_UP]:      self.cars[0].backward()
        elif self.player == 'computer':
            pass
        
        self.sprites.update()
        
        self.clock.tick(60)
    
    def draw(self):
        # Clear screen
        try:
            for rect in self.cleanup_rects:
                self.screen.blit(self.background, rect, rect)
        except:
            pass
        self.sprites.clear(self.screen, self.background)
        
        # Draw sprites
        dirty = self.sprites.draw(self.screen)
        
        # LiDaRs are drawn on top of the cars
        self.cleanup_rects = []
        car = sorted(self.cars)[-1]
        for l, r in zip(car.lidars, car.measurement):
            l = (l + np.pi * car.a / 180) % (2 * np.pi)
            tmp = pg.draw.line(self.screen, (3, 152, 252), (car.x, car.y), (r * np.sin(l) + car.x, r * np.cos(l) + car.y))
            dirty.append(tmp)
            self.cleanup_rects.append(tmp)
            
        pg.display.update(dirty)

    def cleanup(self):
        pg.quit()
import pygame as pg
from scripts import ComputerCar, PlayerCar, Track
from scripts.text import *
import numpy as np
import os

class Engine:
    pg.font.init()
    font1 = pg.font.SysFont('calibri', 26, bold=True)
    
    def __init__(self, level: str, n_cars: int = 1, player: str = 'player'):
        super().__init__()
        pg.init()
        
        # Setters
        self.track = Track(level)
        self.w, self.h = self.track.w, self.track.h
        self.player = player
        pg.display.set_caption(f'Gene Racer - {self.track.name}')
        # self.logo = pg.image.load(os.path.join(os.environ['GAME_DIR'], f'engine\images\logo32x32.png'))
        # pg.display.set_icon(self.logo)
        self.screen = pg.display.set_mode((self.w, self.h))
        self.running = False
        self.background = pg.Surface(self.screen.get_size())
        self.background.blit(self.track.texture.convert(), (0, 0))
        self.screen.blit(self.background, (0, 0))
        self.clock = pg.time.Clock()
        self.prev_best = ('------', 0)
        
        if self.player == 'player':
            self.cars = [PlayerCar(self) for _ in range(n_cars)]
        elif self.player == 'computer':
            self.cars = [ComputerCar(self) for _ in range(n_cars)]
            self.epoch = 1
        
        # Sprites
        self.car_sprites = pg.sprite.Group(self.cars)
        self.txt_sprites = pg.sprite.Group(ScoreText(self))
        if self.player == 'computer':
            EpochText(self).add(self.txt_sprites)
            BestScoreText(self).add(self.txt_sprites)
            print(f"================ EPOCH {self.epoch} =================")
    
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
            if all(not car.alive for car in self.cars):
                self.epoch += 1
                
                champion = sorted(self.cars)[-1]
                self.prev_best = (champion.name, champion.score)
                tmp = [champion.copy()]
                tmp[-1].name = champion.name
                
                # Create new cars
                s = sum([car.score for car in self.cars])
                for _ in range(len(self.cars) - 1):
                    c = 0
                    try:
                        r = np.random.randint(0, s)
                    except ValueError:
                        print([car.score for car in self.cars])
                        return
                    for car in self.cars:
                        c += car.score
                        if c >= r:
                            tmp.append(car.copy_mutated(float(os.environ['MUTATION_RATE'])))
                            break
                
                for car in tmp:
                    car.kill()
                self.car_sprites.empty()
                del self.cars[:]
                
                self.screen.blit(self.background, (0, 0))
                pg.display.flip()
                
                self.cars = tmp.copy()
                del tmp[:]
                
                self.car_sprites.add(self.cars)
                print(f"================ EPOCH {self.epoch} =================")
                        
        
        self.car_sprites.update()
        self.txt_sprites.update()
        
        self.clock.tick(60)
    
    def draw(self):
        # Clear screen
        self.screen.blit(self.background, (0, 0))
        
        # Draw sprites
        self.txt_sprites.draw(self.screen)
        self.car_sprites.draw(self.screen)
        
        # LiDaRs are drawn on top of the cars
        car = sorted(self.cars, key = lambda x: x.score if x.alive else -1)[-1]
        for l, r in zip(car.lidars, car.measurement):
            l = (l + np.pi * car.a / 180) % (2 * np.pi)
            pg.draw.line(self.screen, (3, 152, 252), (car.x, car.y), (r * np.sin(l) + car.x, r * np.cos(l) + car.y))
            
        pg.display.flip()

    def cleanup(self):
        champion = sorted(self.cars)[-1]
        champion.brain.save(f'{self.track.name}-{self.epoch - 1}-{champion.name}')
        
        pg.quit()
import numpy as np
import pygame
import math

FPS = 60
SCREEN_SIZE = 1000

thrust = 12000
dt = 1 / FPS

class Lander:
    def __init__(self):
        self.velocity = [0.0, 0.0]
        self.verticies = [500.0, 200.0]
        self.top = [35, -70]
        
        self.weight = 4570
        self.fuel = 10075 - self.weight
        
    def update_velocity(self):
        velocity = np.array(self.velocity)
        verticies = np.array(self.verticies)
        
        velocity[1] -= 1.62 / FPS
        
        if (self.get_floor()):
            velocity[1] = max(velocity[1], 0)
    
        verticies[0] -= velocity[0]
        verticies[1] -= velocity[1]
        
        verticies[1] = min(verticies[1], SCREEN_SIZE - 70)
                
        self.verticies = verticies
        self.velocity = velocity
        
        self.画()
      
    def get_floor(self):
        return self.verticies[1] == SCREEN_SIZE - 70
      
    def thrust(self):
        velocity = (thrust / self.get_weight()) * dt
                
        self.velocity[1] += velocity
        
        self.fuel -= 100
      
    def get_weight(self):
        return self.weight + max(self.fuel, 0)
    
    def get_verticie_pos(self, x, y):
        return (self.verticies[0] - 50 + self.top[0] + x, self.verticies[1] - 50 + self.top[1] + y)
    
    def 画(self):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.verticies[0] - 50, self.verticies[1] - 30, 100, 30))
        
        scale = 30
        
        pygame.draw.polygon(screen, (255, 255, 255), [
            self.get_verticie_pos(-scale, 2 * scale),
            self.get_verticie_pos(-scale, scale),
            self.get_verticie_pos(0, 0),
            self.get_verticie_pos(scale, 0),
            self.get_verticie_pos(2 * scale, scale),
            self.get_verticie_pos(2 * scale, 2 * scale),
            self.get_verticie_pos(scale, 3 * scale),
            self.get_verticie_pos(0, 3 * scale)
        ])
    
pygame.init()
    
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
run = True

clock = pygame.time.Clock()
lander = Lander()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, SCREEN_SIZE - 70, SCREEN_SIZE, 70))
    
    if (pygame.key.get_pressed()[pygame.K_UP]):
        lander.thrust()
    
    lander.update_velocity()
    
    clock.tick(FPS)
        
    pygame.display.flip()
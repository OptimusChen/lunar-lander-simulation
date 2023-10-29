import numpy as np
import pygame
import math

import random

FPS = 60
SCREEN_SIZE = 1000
PARTICLE_COUNT = 4

GOLD = (255, 215, 0)

# unit: N
thrust = 25000

max_speed = 5

dt = 1 / FPS

particles = []

colors = [(255, 150, 0), (255, 255, 0), (255, 0, 0)]
# colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        particles.append(self)
    
    def update(self):
        rx = random.randint(-5, 5)
        ry = random.randint(5, 10)
        
        self.x += rx
        self.y += ry
        
        if (self.y > SCREEN_SIZE - 70):
            particles.remove(self)
        
        pygame.draw.rect(screen, colors[random.randint(0, len(colors) - 1)], pygame.Rect(self.x, self.y, 5, 5))

class Lander:
    def __init__(self):
        self.velocity = [0.0, 0.0]
        self.verticies = [500.0, 200.0]
        
        self.top_verticies = [35, -70]
        self.top_velocity = [0, 0]
                
        # unit: kg
        self.mass = 4570
        self.fuel = 10075 - self.mass
        
        self.leg_height = 30
        
        self.floor = False
        self.crashed = False
        self.success = False
            
        scale = 30

        self.octogon = [
            (-scale, 2 * scale),
            (-scale, scale),
            (0, 0),
            (scale, 0),
            (2 * scale, scale),
            (2 * scale, 2 * scale)
        ]
        
    def update_velocity(self):
        self.fuel = max(self.fuel, 0)
        
        velocity = np.array(self.velocity)
        verticies = np.array(self.verticies)
        
        velocity[1] -= 1.62 / FPS
        
        if self.get_floor():
            if not self.floor:
                self.floor = True
                
                self.impact()
            
            velocity[1] = max(velocity[1], 0)
        else:
            self.floor = False
    
        verticies[0] -= velocity[0]
        verticies[1] -= velocity[1]
        
        verticies[1] = min(verticies[1], SCREEN_SIZE - 70)
                
        self.verticies = verticies
        self.velocity = velocity
        
        self.top_verticies[0] -= self.top_velocity[0]
        self.top_verticies[1] -= self.top_velocity[1]
        
        self.draw()
      
    def get_floor(self):
        return self.verticies[1] == SCREEN_SIZE - 70
      
    def thrust(self):
        if self.fuel <= 0 or self.crashed or self.success:
            return
        
        velocity = (thrust / self.get_mass()) * dt
                
        self.velocity[1] += velocity
        
        for i in range(PARTICLE_COUNT):
            Particle(self.verticies[0], self.verticies[1] - self.leg_height)
        
        self.fuel -= 10
      
    def get_mass(self):
        return self.mass + max(self.fuel, 0)
    
    def get_octogon_coords(self):
        coords = []
        
        for coord in self.octogon:
            coords.append((self.verticies[0] - 50 + self.top_verticies[0] + coord[0], self.verticies[1] - 20 - self.leg_height + self.top_verticies[1] + coord[1]))
        
        return coords
    
    def get_mph(self):
        return abs(self.velocity[1] * 2.23694)
    
    def get_mph_string(self):
        return f'{self.get_mph():.2f}'
    
    def launch(self):
        self.top_velocity[1] += 30
        
    def impact(self):        
        if self.get_mph() > max_speed:
            print("failed")
            
            self.crashed = True
            self.leg_height = 0
        else:
            print("passed")
            
            self.success = True
    
    def draw(self):
        pygame.draw.rect(screen, GOLD, pygame.Rect(self.verticies[0] - 50, self.verticies[1] - 30 - self.leg_height, 100, 30))
                
        # legs
        pygame.draw.line(screen, GOLD, (self.verticies[0], self.verticies[1] - self.leg_height), (self.verticies[0], self.verticies[1]), 4)
        pygame.draw.line(screen, GOLD, (self.verticies[0] - 20, self.verticies[1] - self.leg_height), (self.verticies[0] - 40, self.verticies[1]), 4)
        pygame.draw.line(screen, GOLD, (self.verticies[0] + 20, self.verticies[1] - self.leg_height), (self.verticies[0] + 40, self.verticies[1]), 4)
                
        pygame.draw.polygon(screen, (200, 200, 200), self.get_octogon_coords())
    
def draw_text(text, color, x = -1, y = -1, width = -1, height = -1, edit_dimensions = False, offset = (0, 0)):
    text_display = font.render(text, True, color)

    rect = text_display.get_rect()

    if edit_dimensions:
        rect.center = (x, y)
        rect.width = width
        rect.height = height
    
    rect.centerx -= offset[0]
    rect.centery -= offset[1]
    
    screen.blit(text_display, rect)
    
pygame.init()
    
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
run = True

clock = pygame.time.Clock()
lander = Lander()

font = pygame.font.Font('freesansbold.ttf', 32)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                lander.launch()
            if (event.key == pygame.K_r):
                lander = Lander()
                
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, SCREEN_SIZE - 70, SCREEN_SIZE, 70))
    
    if (pygame.key.get_pressed()[pygame.K_UP]):
        lander.thrust()
    
    lander.update_velocity()
    
    draw_text("Fuel: " + str(lander.fuel), (255, 255, 255))
    draw_text('MPH: ' + lander.get_mph_string(), (255, 0, 0) if lander.get_mph() > max_speed or lander.crashed else (0, 255, 0), offset=(0, -30))
    
    if (lander.success):
        draw_text('SUCCESS!!1!!111', (0, 255, 0), SCREEN_SIZE / 2, SCREEN_SIZE / 2, 30, 30, True)
        draw_text('R to restart', (255, 255, 255), SCREEN_SIZE / 2, SCREEN_SIZE / 2 + 60, 30, 30, True)
    
    if (lander.crashed):
        draw_text('FAIL!!1!!111', (255, 0, 0), SCREEN_SIZE / 2, SCREEN_SIZE / 2, 30, 30, True)
        draw_text('R to restart', (255, 255, 255), SCREEN_SIZE / 2, SCREEN_SIZE / 2 + 60, 30, 30, True)

    for particle in particles:
        particle.update()
        
    clock.tick(FPS)
        
    pygame.display.flip()

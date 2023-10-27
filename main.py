import numpy as np
import pygame
import math

import random

FPS = 60
SCREEN_SIZE = 1000
PARTICLE_COUNT = 4

GOLD = (255, 215, 0)

thrust = 25000
leg_height = 30

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
                
        self.mass = 4570
        self.fuel = 10075 - self.mass

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
        
        if (self.get_floor()):
            velocity[1] = max(velocity[1], 0)
    
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
        if (self.fuel <= 0):
            return
        
        velocity = (thrust / self.get_mass()) * dt
                
        self.velocity[1] += velocity
        
        for i in range(PARTICLE_COUNT):
            Particle(self.verticies[0], self.verticies[1] - leg_height)
        
        self.fuel -= 10
      
    def get_mass(self):
        return self.mass + max(self.fuel, 0)
    
    def get_octogon_coords(self):
        coords = []
        
        for coord in self.octogon:
            coords.append((self.verticies[0] - 50 + self.top_verticies[0] + coord[0], self.verticies[1] - 20 - leg_height + self.top_verticies[1] + coord[1]))
        
        return coords
    
    def get_mph(self):
        return abs(self.velocity[1] * 2.23694)
    
    def get_mph_string(self):
        return f'{self.get_mph():.2f}'
    
    def launch(self):
        self.top_velocity[1] += 30
    
    def draw(self):
        pygame.draw.rect(screen, GOLD, pygame.Rect(self.verticies[0] - 50, self.verticies[1] - 30 - leg_height, 100, 30))
                
        pygame.draw.line(screen, GOLD, (self.verticies[0], self.verticies[1] - leg_height), (self.verticies[0], self.verticies[1]), 4)
        pygame.draw.line(screen, GOLD, (self.verticies[0] - 20, self.verticies[1] - leg_height), (self.verticies[0] - 40, self.verticies[1]), 4)
        pygame.draw.line(screen, GOLD, (self.verticies[0] + 20, self.verticies[1] - leg_height), (self.verticies[0] + 40, self.verticies[1]), 4)
                
        pygame.draw.polygon(screen, (200, 200, 200), self.get_octogon_coords())
    
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
                
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, SCREEN_SIZE - 70, SCREEN_SIZE, 70))
    
    if (pygame.key.get_pressed()[pygame.K_UP]):
        lander.thrust()
    
    lander.update_velocity()
    
    fuel_display = font.render("Fuel: " + str(lander.fuel), True, (255, 255, 255))
    screen.blit(fuel_display, fuel_display.get_rect())
    
    speed_display = font.render('MPH: ' + lander.get_mph_string(), True, (255, 255, 255))
    
    speed_display_rect = speed_display.get_rect()
    speed_display_rect.centery += 30
    
    screen.blit(speed_display, speed_display_rect)

    for particle in particles:
        particle.update()
        
    clock.tick(FPS)
        
    pygame.display.flip()

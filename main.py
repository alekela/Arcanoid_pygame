import pygame
from classes import Ball, Platform, Brick

w = 600
h = 600
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.draw.rect(screen, 'white', [1, 1, w - 2, h - 2], 2)

running = True
ball = Ball(screen, 300, 494)
fps = 10
clock = pygame.time.Clock()
while running:
    clock.tick(1000 // fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ball.update(screen, 1 / fps)
    pygame.display.flip()

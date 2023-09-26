import pygame
from classes import Ball, Platform, Brick

w = 600
h = 600
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.draw.rect(screen, 'white', [1, 1, w - 2, h - 2], 2)

running = True
ball = Ball(screen, 300, 494)
platform = Platform(screen)

fps = 10
clock = pygame.time.Clock()
platform_right = False
platform_left = False
while running:
    clock.tick(1000 // fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                platform_left = True
            if event.key == pygame.K_d:
                platform_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                platform_left = False
            if event.key == pygame.K_d:
                platform_right = False
    if platform_right:
        platform.update(screen, 1)
    if platform_left:
        platform.update(screen, -1)
    ball.update(screen, 1 / fps)
    ball.collide_with_platform(platform)
    running = ball.endgame(screen)
    pygame.draw.rect(screen, 'white', [1, 1, w - 2, h - 2], 2)
    pygame.display.flip()

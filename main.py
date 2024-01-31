import pygame
from classes import Ball, Platform, Level

w = 600
h = 600
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.draw.rect(screen, 'white', [1, 1, w - 2, h - 2], 2)

running = True
ball = Ball(screen, 300, 494)
platform = Platform(screen)
level = Level(screen, 200, 100)


fps = 100
clock = pygame.time.Clock()
platform_right = False
platform_left = False
while running:
    clock.tick(fps)
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
        platform.update_velocity(2)
    if platform_left:
        platform.update_velocity(-2)
    if not (platform_left or platform_right):
        platform.update_velocity(0)

    level.check_all_collisions(ball, platform)
    level.update_figures(ball, platform)
    endgame = level.endgame_check(ball)
    if endgame != 0:
        font = pygame.font.SysFont('comicsans', 30)
        if endgame == 1:
            text = font.render("Congratulations! You've won!!!", True, 'white', 'black')
        else:
            text = font.render("Oh no!!! You've lost! Try again!", True, 'white', 'black')
        textRect = text.get_rect()
        textRect.center = (300, 300)
        screen.blit(text, textRect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()
    level.draw_level()
    pygame.draw.rect(screen, 'white', [1, 1, w - 2, h - 2], 2)
    pygame.display.flip()

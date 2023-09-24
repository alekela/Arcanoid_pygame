import pygame
from random import randint
from numpy import cos, sin, pi


class Ball:
    def __init__(self, field, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        pygame.draw.circle(field, 'white', [x, y], self.radius, 0)
        angle = randint(20, 160) / 180 * pi
        self.Vx = 10 * cos(angle)
        self.Vy = -10 * sin(angle)

    def update(self, field, dt):
        pygame.draw.circle(field, 'black', [self.x, self.y], self.radius, 0)
        self.x += self.Vx * dt
        self.y += self.Vy * dt
        self.check(field)
        pygame.draw.circle(field, 'white', [self.x, self.y], self.radius, 0)

    def check(self, field):
        w, h = field.get_size()
        if 3 + self.radius >= self.x or self.x >= w - 3 - self.radius:
            self.Vx = -self.Vx
        if 3 + self.radius >= self.y or self.y >= h - 3 - self.radius:
            self.Vy = -self.Vy

    def collide_with_platform(self):
        self.Vy = -self.Vy


class Platform:
    def __init__(self, field):
        w, h = field.get_size()
        self.x = w / 2
        self.y = 5 / 6 * h
        self.dy = 10
        self.dx = 50
        pygame.draw.rect(field, 'white', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)

    def get_pos(self):
        return self.x, self.y

    def update(self, field, dx):
        pygame.draw.rect(field, 'black', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)
        self.x += dx
        self.redraw(field)

    def redraw(self, field):
        pygame.draw.rect(field, 'white', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)


class Brick:
    pass



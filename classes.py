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

    def collide_with_platform(self, other):
        other_x, other_y = other.get_pos()
        other_dx, other_dy = other.get_sizes()
        if other_x - other_dx / 2 < self.x < other_x + other_dx / 2:
            if self.y <= other_y + other_dy / 2 and self.y >= other_y - other_dy / 2:
                self.Vy = -self.Vy

    def endgame(self, field):
        return not (self.y >= field.get_size()[1] - 5)


class Platform:
    def __init__(self, field):
        w, h = field.get_size()
        self.x = w / 2
        self.y = 5 / 6 * h
        self.dy = 10
        self.dx = 100
        pygame.draw.rect(field, 'white', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)

    def get_pos(self):
        return self.x, self.y

    def get_sizes(self):
        return self.dx, self.dy

    def update(self, field, dx):
        pygame.draw.rect(field, 'black', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)
        if self.x + dx + self.dx / 2 < field.get_size()[0] - 2 and self.x + dx - self.dx / 2 > 2:
            self.x += dx
        self.redraw(field)

    def redraw(self, field):
        pygame.draw.rect(field, 'white', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)


class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 10
        self.dy = 5

    def get_sizes(self):
        return self.dx, self.dy



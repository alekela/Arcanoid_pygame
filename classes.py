import pygame
from random import randint


class Level:
    def __init__(self, field, brick_sizex, brick_sizey):
        self.field = field
        self.brick_sizex = brick_sizex
        self.brick_sizey = brick_sizey

        w, h = self.field.get_size()
        self.bw = w * 4 // 5 // self.brick_sizex
        self.bh = h // 3 // self.brick_sizey
        self.bricks = [[1 for _ in range(self.bw)] for _ in range(self.bh)]

        if self.bw % 2 == 0:
            self.start_point = (w // 2 - self.bw // 2 * self.brick_sizex, 0.05 * h)
        else:
            self.start_point = (w // 2 - (self.bw // 2 + 0.5) * self.brick_sizex, 0.05 * h)   # start point for drawing bricks

        self.draw_level()

    def draw_level(self):
        for i in range(self.bh):
            for j in range(self.bw):
                if self.bricks[i][j]:
                    self.draw_brick(j, i)

    def draw_brick(self, x, y):
        pygame.draw.rect(self.field, 'white',
                         [self.start_point[0] + self.brick_sizex * x + 1,
                          self.start_point[1] + self.brick_sizey * y + 1,
                          self.brick_sizex - 1, self.brick_sizey - 1])

    def erase_brick(self, x, y):
        pygame.draw.rect(self.field, 'black',
                         [self.start_point[0] + self.brick_sizex * x,
                          self.start_point[1] + self.brick_sizey * y,
                          self.brick_sizex, self.brick_sizey])

    def check_collision_ball_platform(self, ball, platform):
        ball_x, ball_y = ball.get_pos()
        ball_r = ball.get_radius()
        plat_x, plat_y = platform.get_pos()
        plat_dx, plat_dy = platform.get_sizes()
        ball_vx, ball_vy = ball.get_velocity()
        if plat_x - plat_dx / 2 < ball_x < plat_x + plat_dx / 2:
            if plat_y - ball_r - plat_dy / 2 < ball_y + ball_vy < plat_y + plat_dy / 2:
                ball.update_velocity(ball_vx - 0.3 * platform.get_velocity(), -ball_vy)

    def check_collision_with_brick(self, ball):
        ball_x, ball_y = ball.get_pos()
        ball_vx, ball_vy = ball.get_velocity()
        flag = False
        for i in range(self.bh):
            for j in range(self.bw):
                if self.bricks[i][j]:
                    if self.start_point[1] + self.brick_sizey * i - ball.get_radius() <= ball_y + ball_vy <= \
                            self.start_point[1] + self.brick_sizey * (i + 1) + ball.get_radius():
                        if self.start_point[0] + self.brick_sizex * j - ball.get_radius() <= ball_x + ball_vx <= \
                                self.start_point[0] + self.brick_sizex * (j + 1) + ball.get_radius():
                            self.erase_brick(j, i)
                            self.bricks[i][j] = 0
                            flag = True
                            if ball_y > self.start_point[1] + self.brick_sizey * (i + 1) + ball.get_radius() \
                                    or ball_y < self.start_point[1] + self.brick_sizey * i - ball.get_radius():
                                ball.update_velocity(ball_vx, -ball_vy)
                            elif ball_x > self.start_point[0] + self.brick_sizex * (j + 1) + ball.get_radius() \
                                    or ball_x < self.start_point[0] + self.brick_sizex * j - ball.get_radius():
                                ball.update_velocity(-ball_vx, ball_vy)
                            break
            if flag:
                break

    def check_collision_with_walls(self, ball):
        w, h = self.field.get_size()
        x, y = ball.get_pos()
        radius = ball.get_radius()
        vx, vy = ball.get_velocity()
        if 2 + radius >= x + vx or x + vx >= w - 2 - radius:
            ball.update_velocity(-vx, vy)
        if 2 + radius >= y + vy:
            ball.update_velocity(vx, -vy)

    def endgame_check(self, ball):
        ball_y = ball.get_pos()[1]
        ball_vy = ball.get_velocity()[1]
        check1 = False
        for i in self.bricks:
            if 1 in i:
                check1 = True

        if check1 and ball_y + ball_vy < self.field.get_size()[1] - ball.get_radius():
            return 0
        elif not check1:
            return 1
        elif ball_y + ball_vy >= self.field.get_size()[1] - ball.get_radius():
            return -1

    def update_figures(self, ball, platform):
        ball.update(self.field)
        platform.update(self.field)

    def check_all_collisions(self, ball, platform):
        self.check_collision_with_walls(ball)
        self.check_collision_with_brick(ball)
        self.check_collision_ball_platform(ball, platform)


class Ball:
    def __init__(self, field, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        pygame.draw.circle(field, 'white', [x, y], self.radius, 0)
        self.Vx = randint(1, 3) / 2
        self.Vy = -randint(3, 4) / 2

    def get_pos(self):
        return self.x, self.y

    def get_radius(self):
        return self.radius

    def get_velocity(self):
        return self.Vx, self.Vy

    def update_velocity(self, vx, vy):
        self.Vx = vx
        self.Vy = vy

    def update(self, field):
        pygame.draw.circle(field, 'black', [self.x, self.y], self.radius, 0)
        self.x += self.Vx
        self.y += self.Vy
        pygame.draw.circle(field, 'white', [self.x, self.y], self.radius, 0)


class Platform:
    def __init__(self, field):
        w, h = field.get_size()
        self.x = w / 2
        self.y = 5 / 6 * h
        self.dy = 10
        self.dx = 100
        self.Vx = 0
        pygame.draw.rect(field, 'white', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)

    def get_pos(self):
        return self.x, self.y

    def get_sizes(self):
        return self.dx, self.dy

    def get_velocity(self):
        return self.Vx

    def update_velocity(self, vx):
        self.Vx = vx

    def update(self, field):
        pygame.draw.rect(field, 'black', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)
        if self.x + self.Vx + self.dx / 2 < field.get_size()[0] - 2 and self.x + self.Vx - self.dx / 2 > 2:
            self.x += self.Vx
        pygame.draw.rect(field, 'white', [self.x - self.dx / 2, self.y - self.dy / 2, self.dx, self.dy], 0)

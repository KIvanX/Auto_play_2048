import random
import time
import pygame


class Table_2048:
    def __init__(self, window, sx, sy, anim_speed):
        self.window = window
        self.sx, self.sy = sx, sy
        self.score, self.anim_speed = 0, anim_speed
        self.sides = ['left', 'right', 'top', 'bottom']
        self.font = pygame.font.SysFont('serif', 50)
        self.font_end = pygame.font.SysFont('serif', 100)
        self.colors = {0: (200, 200, 200), 2: (250, 250, 150), 4: (150, 150, 250), 8: (250, 150, 250),
                       16: (150, 150, 50), 32: (50, 50, 150), 64: (150, 50, 150), 128: (250, 150, 0),
                       256: (0, 150, 150), 512: (250, 0, 150), 1024: (50, 250, 50), 2048: (250, 0, 0),
                       4096: (100, 0, 200)}
        self.a = [[0]*4 for _ in range(4)]
        self.end = False
        for _ in range(2):
            self.add_element(self.a, anim=False)

    def add_element(self, arr, anim=True):
        free = [(i, j) for i in range(4) for j in range(4) if not arr[i][j]]

        i, j = random.choice(free)
        if anim:
            for dl in range(0, 110, 10):
                self.show()
                self.draw_block(i*100, j*100, 2, size=dl)
                pygame.display.flip()
                time.sleep(1 / self.anim_speed)
        arr[i][j] = 2

    def step(self, side, arr=None):
        if self.end:
            return 0
        edited = False
        is_real, arr = (True, self.a) if not arr else (False, arr)
        dx, dy = {'left': (-1, 0), 'right': (1, 0), 'top': (0, -1), 'bottom': (0, 1)}[side]
        for _ in range(3):
            to_move, act = [], []
            for i in range(4):
                for j in range(4):
                    if arr[i][j] and 0 <= i + dx < 4 and 0 <= j + dy < 4:
                        if not arr[i + dx][j + dy]:
                            to_move.append((i, j))
                        if arr[i][j] == arr[i + dx][j + dy] and (i + dx, j + dy) not in act and (i, j) not in act:
                            to_move.append((i, j))
                            act.append((i + dx, j + dy))

            if is_real:
                for dl in range(0, 100, max(1, int(0.08 * self.anim_speed))):
                    pygame.draw.rect(self.window, (250, 250, 250), (self.sx, self.sy, 400, 400), border_radius=10)
                    pygame.draw.rect(self.window, (250, 250, 250), (self.sx - 2, self.sy - 2, 404, 404), 2,
                                     border_radius=10)
                    for i in range(4):
                        for j in range(4):
                            self.draw_block(i * 100, j * 100, arr[i][j] if (i, j) not in to_move else 0)

                    for i in range(4):
                        for j in range(4):
                            if (i, j) in to_move:
                                self.draw_block(i * 100 + dl * dx, j * 100 + dl * dy, arr[i][j])
                    pygame.display.flip()

            edited = True if to_move else edited
            for i, j in to_move:
                if is_real:
                    self.score += arr[i + dx][j + dy] * 2
                arr[i + dx][j + dy], arr[i][j] = arr[i][j] + arr[i + dx][j + dy], 0

        if edited:
            self.add_element(arr, anim=is_real)

        if is_real and self.check_finish():
            self.end = True

        return edited

    def show(self):
        pygame.draw.rect(self.window, (250, 250, 250), (self.sx, self.sy, 400, 400), border_radius=10)
        pygame.draw.rect(self.window, (250, 250, 250), (self.sx - 2, self.sy - 2, 404, 404), 2, border_radius=10)
        for i in range(4):
            for j in range(4):
                self.draw_block(i * 100, j * 100, self.a[i][j])

        if self.end:
            end_text = self.font_end.render('Конец', True, (250, 0, 50))
            self.window.blit(end_text, (self.sx + 75, self.sy + 125))

    def check_finish(self):
        for side in self.sides:
            if self.step(side, arr=[list(self.a[i]) for i in range(4)]):
                return False
        return True

    def draw_block(self, x_pos, y_pos, num, size=100):
        x_pos, y_pos = self.sx + x_pos, self.sy + y_pos
        pygame.draw.rect(self.window, self.colors[num], (x_pos, y_pos, size, size), border_radius=10)
        pygame.draw.rect(self.window, (0, 0, 0), (x_pos, y_pos, size, size), 1, 10)
        num_text = self.font.render(str(num), True, (0, 0, 0))
        if num and size == 100:
            self.window.blit(num_text, (x_pos + 35 - (len(str(num)) - 1) * 12, y_pos + 20))

    def auto_step(self):
        res = [(self.recursion([self.sides[i]]), i) for i in range(4)]
        for _, ind in sorted(res)[::-1]:
            if self.step(self.sides[ind]):
                return 0
        self.end = True

    def recursion(self, way):
        if len(way) == 4:
            arr = [list(self.a[i]) for i in range(4)]
            for side in way:
                self.step(side, arr=arr)
            return sum([line.count(0) for line in arr]) + sum([el**2 for line in arr for el in line]) / 10**8

        res = []
        for side in self.sides:
            res.append(self.recursion(way + [side]))
        return max(res)


pygame.init()
screen = pygame.display.set_mode((420, 480))
pygame.display.set_caption('2048')
font = pygame.font.SysFont('roman', 40)
screen.fill((200, 200, 250))

table = Table_2048(screen, 10, 10, 100)
table.show()

show, auto_game = True, False
while show:
    if auto_game:
        table.auto_step()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            show = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 275 < x < 395 and 430 < y < 465:
                auto_game = not auto_game
                table.anim_speed = 1000 if auto_game else 100

            if 150 < x < 270 and 430 < y < 465:
                table = Table_2048(screen, 10, 10, 100)
                auto_game = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                table.step('left')
            if e.key == pygame.K_RIGHT:
                table.step('right')
            if e.key == pygame.K_UP:
                table.step('top')
            if e.key == pygame.K_DOWN:
                table.step('bottom')

    screen.fill((200, 200, 250))
    screen.blit(font.render(str(table.score), True, (0, 0, 0)), (30, 420))
    pygame.draw.rect(screen, (150, 150, 250), (275, 430, 120, 35), border_radius=20)
    screen.blit(font.render('авто', True, (0, 0, 0)), (300, 420))
    pygame.draw.rect(screen, (150, 150, 250), (150, 430, 120, 35), border_radius=20)
    screen.blit(font.render('снова', True, (0, 0, 0)), (160, 420))
    table.show()
    pygame.display.flip()

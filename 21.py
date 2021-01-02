import pygame
import pyganim
from pygame import *


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2
    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)


def pause():
    font = pygame.font.Font(None, 50)
    text = font.render("Paused", True, [255, 255, 0])
    textpos = (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50)
    screen.blit(text, textpos)
    paused = True
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        timer.tick(25)


def game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, [255, 255, 0])
    textpos = (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50)
    text1 = font.render("You died", True, [255, 255, 0])
    textpos1 = (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100)
    text2 = font.render("PRESS ESC", True, [255, 255, 0])
    textpos2= (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 150)
    screen.blit(text, textpos)
    screen.blit(text1, textpos1)
    screen.blit(text2, textpos2)
    paused = True
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        timer.tick(25)
def main():
    pygame.init()
    hero = Player(410, 95)
    mob = Mob(500, 100)
    entities.add(hero)
    entities.add(mob)
    left = right = False
    up = down = False
    weapon = 1 # Создаем окошко
    pygame.display.set_caption("First top game") # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT)) # Создание видимой поверхности
    bg.fill(Color(BACKGROUND_COLOR))
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT
    camera = Camera(camera_configure, total_level_width, total_level_height)
    while 1:
        if not door:
            timer.tick(20)
            pos = ('', '')
            if GAME_OVER == True:
                game_over()
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    pos = e.pos
                if e.type == KEYUP and e.key == K_1:
                    weapon = 1
                if e.type == KEYUP and e.key == K_2:
                    weapon = 2
                if e.type == KEYDOWN and e.key == K_p:
                    pause()
            screen.blit(bg, (0, 0))
            n = camera.get_cord()
            hero.update(left, right, up, down, pos, weapon - 1, n, platforms)
            mob.update(hero)
            for i in bullets:
                i.update(mob)
            camera.update(hero)
            for e in entities:
                screen.blit(e.image, camera.apply(e))
            pygame.display.update()


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        boltAnim = []
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.hp = 100
        self.yvel = 0  # скорость вертикального перемещения
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill('white')
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        for anim in ANIMATION_STAY:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltStay = pyganim.PygAnimation(boltAnim)
        self.boltStay.play()
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

    def get_cord(self):
        return (self.rect.x, self.rect.y)

    def update(self, left, right, up, down, pos, weap, n, platforms):
        global GAME_OVER
        if self.hp <= 0:
            GAME_OVER = True
        if pos != ('', ''):
            self.weapon(pos, weap, n)

        if left and not right:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right and not left:
            self.xvel = MOVE_SPEED
            self.image.set_colorkey("WHITE")
            self.boltAnimRight.blit(self.image, (0, 0))
        if not (left or right):
            self.xvel = 0

        if not (up or down):
            self.yvel = 0

        if (not (left or right)) and (not (up or down)):
            self.image.set_colorkey("WHITE")
            self.boltStay.blit(self.image, (0, 0))
        if up:
            self.yvel = -MOVE_SPEED
        if down:
            self.yvel = +MOVE_SPEED
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def weapon(self, pos, weap, n):
        bullet = Bullet(self.rect.x + 15, self.rect.y + 15, pos[0], pos[1], INVENTORY[weap], n)
        entities.add(bullet)
        bullets.add(bullet)

    def minus_hp(self, n):
        self.hp -= n
        self.rect.x -= 30

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if xvel > 0:  # вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Mob(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill('red')
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.hp = 100

    def get_cord(self):
        return (self.rect.x, self.rect.y)

    def update(self, hero):
        if self.hp <= 0:
            self.kill()
        else:
            self.collide(hero)

    def collide(self, hero):
        if sprite.collide_rect(self, hero):
            hero.minus_hp(20)

    def minus_hp(self, n):
        self.hp -= n


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1, type, n):
        import math
        pygame.sprite.Sprite.__init__(self)
        self.style = INVENTORY_PROP[type][0]
        self.dist = INVENTORY_PROP[type][1]
        print(self.dist)
        self.y = y
        self.x = x
        self.cam_pos = n
        self.mouse_x = x1 + abs(self.cam_pos[0])
        self.mouse_y = y1 + abs(self.cam_pos[1])
        self.speed = 6
        self.power = INVENTORY_PROP[type][2]
        self.being_in_the_list = 0
        if self.style == 'line':
            self.image = pygame.Surface((15, 10), pygame.SRCALPHA)
            pygame.draw.circle(self.image, pygame.Color('yellow'), (7, 5), 5)
            self.rect = self.image.get_rect()
            self.side_x = self.mouse_x - self.x
            self.side_y = self.mouse_y - self.y
            self.hyp = math.hypot(self.side_x, self.side_y)
            self.sin = abs(self.side_y) / self.hyp
            self.cos = abs(self.side_x) / self.hyp
            self.degree = math.degrees(math.asin(self.sin))
            if self.hyp > self.dist:
                self.hyp = self.dist
                self.side_y = self.hyp * math.sin(math.radians(self.degree)) * (1 if self.side_y >= 0 else -1)
                self.side_x = self.hyp * math.cos(math.radians(self.degree)) * (1 if self.side_x >= 0 else -1)
            self.list_of_line_coordinates = self.get_line(x, y,
                                                          x + int(self.side_x),
                                                          y + int(self.side_y))
        else:
            self.image = pygame.Surface((self.dist, self.dist), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            pygame.draw.circle(self.image, pygame.Color('Blue'), (self.dist // 2, self.dist // 2), self.dist // 2, 2)

    def update(self, mob):
        if self.style == 'line':
            try:
                self.rect.x = self.list_of_line_coordinates[self.being_in_the_list][0]
                self.rect.y = self.list_of_line_coordinates[self.being_in_the_list][1]
                self.being_in_the_list += self.speed
                for p in platforms:
                    if sprite.collide_rect(self, p):
                        self.kill()
                if sprite.collide_rect(self, mob):
                    mob.minus_hp(self.power)
                    self.kill()
            except IndexError:
                self.kill()
        else:
            self.rect.x = self.x - self.dist // 2
            self.rect.y = self.y - self.dist // 2
            for p in platforms:
                if sprite.collide_rect(self, p):
                    self.kill()
            if sprite.collide_rect(self, mob):
                mob.minus_hp(self.power)
                self.kill()

    def get_line(self, x1, y1, x2, y2):
        points = []
        issteep = abs(y2 - y1) > abs(x2 - x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2 - y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        if rev:
            points.reverse()
        return points




class Platform(sprite.Sprite):
    def __init__(self, x, y, status):
        sprite.Sprite.__init__(self)
        if status == 'wall':
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image = image.load("block/wall.png")
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        elif status == 'tree':
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image = image.load("block/Tree.png")
            self.image.set_colorkey("WHITE")
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        elif status == 'build':
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image = image.load("block/build.png")
            self.image.set_colorkey("WHITE")
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        elif status == 'top':
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image = image.load("block/top.png")
            self.image.set_colorkey("WHITE")
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        elif status == 'window':
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image = image.load("block/window.png")
            self.image.set_colorkey("WHITE")
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        elif status == 'door':
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image = image.load("block/door.png")
            self.image.set_colorkey("WHITE")
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Door(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("block/door.png")
        self.image.set_colorkey("WHITE")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Floor(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("block/floor1.png")
        self.image.set_colorkey("WHITE")
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def get_cord(self):
        return self.state.topleft

WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
INVENTORY = ['gun', 'sword']
bullets = pygame.sprite.Group()
INVENTORY_PROP = {'gun': ['line', 200, 20], 'sword': ['circle', 50, 50]}
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
PLATFORM_WIDTH = 32
ANIMATION_DELAY = 1
ANIMATION_STAY = [('block/Player/pass1.png'), ('block/Player/pass2.png')]
ANIMATION_RIGHT = [('block/Player/go_r_l.png'),
                   ('block/Player/go_r_stay.png'),
                   ('block/Player/go_r_r.png'),
                   ('block/Player/go_r_stay.png')]
PLATFORM_HEIGHT = 32
door = False
floor = []
timer = pygame.time.Clock()
entities = pygame.sprite.Group()
platforms = []
doors = []
level = [
        "----------------------------------",
        "- kkkkkkk          ***********   -",
        "- bbbbbbb                        -",
        "- b+bbb+b                        -",
        "- bbbdbbb    --                  -",
        "-                                -",
        "---   -------------------        -",
        "-                                -",
        "-         ------------------------",
        "-                                -",
        "-------------------------        -",
        "-                                -",
        "-        -------------------------",
        "-                                -",
        "-                                -",
        "-      -                         -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "-                                -",
        "- kkkkkkk                        -",
        "- bbbbbbb                        -",
        "- b+bbb+b                        -",
        "- bbbdbbb    --                  -",
        "-                                -",
        "---   -------------------        -",
        "-                                -",
        "-         ------------------------",
        "-                                -",
        "-------------------------        -",
        "-                                -",
        "-        -------------------------",
        "-                                -",
        "-                                -",
        "-      -                         -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]
level1 = [
        "----------------------------------",
        "-                  ***********   -",
        "-                                -",
        "-  kkkkk                         -",
        "-  bbdbb     --                  -",
        "-                                -",
        "---   -------------------        -",
        "-                                -",
        "-         ------------------------",
        "-                                -",
        "-------------------------        -",
        "-                                -",
        "-        -------------------------",
        "-                                -",
        "-                                -",
        "-      -                         -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "-                                -",
        "- kkkkkkk                        -",
        "- bbbbbbb                        -",
        "- b+bbb+b                        -",
        "- bbbdbbb    --                  -",
        "-                                -",
        "---   -------------------        -",
        "-                                -",
        "-         ------------------------",
        "-                                -",
        "-------------------------        -",
        "-                                -",
        "-        -------------------------",
        "-                                -",
        "-                                -",
        "-      -                         -",
        "-                                -",
        "-                                -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]

x = y = 0
for row in level:  # вся строка
    for col in row:  # каждый символ
        if col == "-":
            pf = Platform(x, y, 'wall')
            entities.add(pf)
            platforms.append(pf)
        elif col == '*':
            pf = Platform(x, y, 'tree')
            entities.add(pf)
            platforms.append(pf)
        elif col == 'b':
            pf = Platform(x, y, 'build')
            entities.add(pf)
            platforms.append(pf)
        elif col == 'k':
            pf = Platform(x, y, 'top')
            entities.add(pf)
            platforms.append(pf)
        elif col == 'd':
            pf = Door(x, y)
            entities.add(pf)
            doors.append(pf)
        elif col == '+':
            pf = Platform(x, y, 'window')
            entities.add(pf)
            platforms.append(pf)
        elif col == ' ':
            pf = Floor(x, y)
            entities.add(pf)
        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT  # то же самое и с высотой
    x = 0
MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
GRAVITY = 0.35
JUMP_POWER = 10
GAME_OVER = False
screen = pygame.display.set_mode(DISPLAY)
if __name__ == "__main__":
    main()
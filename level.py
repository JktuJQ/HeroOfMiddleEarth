from map import *
from objects import *


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_map(self, map):
        return map.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Test')

        self.clock = pygame.time.Clock()
        self.tick = self.clock.tick(FPS) / 1000
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        self.sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

    def load_map(self):
        self.map = Map('testMap.tmx')
        self.full_map = self.map.full_map()
        self.map_rect = self.full_map.get_rect()

    def render(self):
        self.screen.blit(self.full_map, self.camera.apply_map(self.map_rect))
        for sprite in self.sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def setup(self):
        self.load_map()
        for object in self.map.tiled_map_data.objects:
            if object.name == 'Player':
                self.player = Player(object.x, object.y, self)
            if object.name == 'Wall':
                Obstacle(object.x, object.y, object.width, object.height, self)
            if object.name == 'Mob':
                Mob(object.x, object.y, self)
        self.camera = Camera(MAP_SIZE[0], MAP_SIZE[1])

    def update(self):
        self.sprites.update()
        self.camera.update(self.player)
        self.render()

    def game_over(self):
        pass

    def run(self):
        self.setup()

        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.player.attack(event.pos)
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_w]:
                self.player.y_speed = -PLAYER_SPEED
            if pressed_keys[pygame.K_s]:
                self.player.y_speed = PLAYER_SPEED
            if pressed_keys[pygame.K_a]:
                self.player.x_speed = -PLAYER_SPEED
            if pressed_keys[pygame.K_d]:
                self.player.x_speed = PLAYER_SPEED

            self.update()

        pygame.quit()

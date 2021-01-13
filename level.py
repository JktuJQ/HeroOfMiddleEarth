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

    def apply_pos(self, pos):
        return pos[0] + abs(self.camera.topleft[0]), pos[1] + abs(self.camera.topleft[1])

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Level:
    def __init__(self, index, game):
        pygame.init()
        pygame.display.set_caption("Hero of MiddleEarth")
        self.index = index
        self.game = game

        self.clock = pygame.time.Clock()
        self.tick = self.clock.tick(FPS) / 1000
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        self.wave_index = 0
        self.sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

    def load_map(self):
        self.map = Map(LEVELS[self.index])
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
                Mob(object.x, object.y, object.type, self)
            if object.name == 'Door':
                self.door = Door(object.x, object.y, object.width, object.height, object.type, self)
        self.camera = Camera(MAP_SIZE[0], MAP_SIZE[1])

    def respawn_mobs(self):
        for object in self.map.tiled_map_data.objects:
            if object.name == 'Mob':
                Mob(object.x, object.y, object.type, self)


class Game:
    def __init__(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def terminate(self):
        self.running = False
        pygame.quit()
        sys.exit(0)

    def setup(self, index):
        self.current_level = Level(index, self)
        self.current_level.setup()

    def update(self):
        if self.current_level.wave_index <= 1:
            if self.current_level.mobs.empty():
                self.current_level.respawn_mobs()
        else:
            self.current_level.door.activated = True
        self.current_level.sprites.update()
        self.current_level.camera.update(self.current_level.player)
        self.current_level.render()

    def set_level(self, index, player_pos_index=0):
        self.running = False
        self.run(index)

    def game_over(self):
        self.terminate()

    def run(self, index):
        try:
            self.setup(index)

            self.running = True
            while self.running:
                self.current_level.clock.tick(FPS)
                if not self.paused:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == pygame.BUTTON_LEFT:
                                self.current_level.player.attack(self.current_level.camera.apply_pos(event.pos))
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == pygame.BUTTON_RIGHT:
                                self.set_level(0)
                pressed_keys = pygame.key.get_pressed()
                if not self.paused:
                    if pressed_keys[pygame.K_w]:
                        self.current_level.player.y_speed = -PLAYER_SPEED
                    if pressed_keys[pygame.K_s]:
                        self.current_level.player.y_speed = PLAYER_SPEED
                    if pressed_keys[pygame.K_a]:
                        self.current_level.player.x_speed = -PLAYER_SPEED
                    if pressed_keys[pygame.K_d]:
                        self.current_level.player.x_speed = PLAYER_SPEED
                if pressed_keys[pygame.K_ESCAPE]:
                    self.terminate()
                self.update()

            pygame.quit()
        except pygame.error:
            pygame.quit()

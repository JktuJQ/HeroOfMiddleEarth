import pygame
import pytmx


WIDTH = 600
HEIGHT = 400
PLAYER_SPEED = 250
TILE_SIZE = 32
FPS = 60
MAP_WIDTH = 50
MAP_HEIGHT = 50
WINDOW_SIZE = (WIDTH, HEIGHT)
MAP_SIZE = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)


class Map:
    def __init__(self, file):
        self.tiled_map_data = pytmx.load_pygame(file)

    def full_map(self):
        full_map = pygame.Surface(MAP_SIZE)
        for layer in self.tiled_map_data.visible_layers:
            if type(layer) == pytmx.TiledTileLayer:
                for x, y, gid in layer:
                    tile = self.tiled_map_data.get_tile_image_by_gid(gid)
                    if tile:
                        full_map.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
        return full_map


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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('test_player.png').convert()
        self.image.set_colorkey((255, 255, 255))

        self.game = game

        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0

    def move(self):
        self.x += self.x_speed * self.game.tick
        self.y += self.y_speed * self.game.tick
        self.rect.x = self.x
        self.collide('x')
        self.rect.y = self.y
        self.collide('y')

    def collide(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.x_speed > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.x_speed < 0:
                    self.x = hits[0].rect.right
                self.x_speed = 0
                self.rect.x = self.x
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.y_speed > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.y_speed < 0:
                    self.y = hits[0].rect.bottom
                self.y_speed = 0
                self.rect.y = self.y


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Test')

        self.clock = pygame.time.Clock()
        self.tick = self.clock.tick(FPS) / 1000
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

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
        self.sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        for object in self.map.tiled_map_data.objects:
            if object.name == 'Player':
                self.player = Player(object.x, object.y, self)
            if object.name == 'Wall':
                self.obstacles.add(Obstacle(object.x, object.y, object.width, object.height, self))
        self.sprites.add(self.player)
        self.camera = Camera(MAP_SIZE[0], MAP_SIZE[1])

    def run(self):
        self.load_map()
        self.setup()
        self.render()

        running = True
        while running:
            self.clock.tick(60)
            self.player.x_speed, self.player.y_speed = 0, 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_w]:
                self.player.y_speed = -PLAYER_SPEED
            if pressed_keys[pygame.K_s]:
                self.player.y_speed = PLAYER_SPEED
            if pressed_keys[pygame.K_a]:
                self.player.x_speed = -PLAYER_SPEED
            if pressed_keys[pygame.K_d]:
                self.player.x_speed = PLAYER_SPEED

            self.player.move()
            self.camera.update(self.player)
            self.render()

        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()

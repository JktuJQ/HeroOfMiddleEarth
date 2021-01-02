import pygame
import pytmx


WIDTH = 600
HEIGHT = 400

PLAYER_SPEED = 250
MOB_SPEED = 200

PLAYER_IMAGE = pygame.image.load('data/test_player.png')
PLAYER_IMAGE.set_colorkey((255, 255, 255))
MOB_IMAGE = pygame.image.load('data/test_player.png')
MOB_IMAGE.set_colorkey((255, 255, 255))

TILE_SIZE = 32
FPS = 60

MAP_WIDTH = 50
MAP_HEIGHT = 50
WINDOW_SIZE = (WIDTH, HEIGHT)
MAP_SIZE = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)


class Map:
    def __init__(self, file):
        self.tiled_map_data = pytmx.load_pygame(f'data/{file}')

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
        pygame.sprite.Sprite.__init__(self, game.sprites)
        self.image = PLAYER_IMAGE

        self.game = game

        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0

    def collide(self, group):
        self.rect.x = self.x
        hits_list = pygame.sprite.spritecollide(self, group, False)
        if hits_list:
            if self.x_speed > 0:
                self.x = hits_list[0].rect.left - self.rect.width
            if self.x_speed < 0:
                self.x = hits_list[0].rect.right
            self.x_speed = 0
            self.rect.x = self.x

        self.rect.y = self.y
        hits_list = pygame.sprite.spritecollide(self, group, False)
        if hits_list:
            if self.y_speed > 0:
                self.y = hits_list[0].rect.top - self.rect.height
            if self.y_speed < 0:
                self.y = hits_list[0].rect.bottom
            self.y_speed = 0
            self.rect.y = self.y

    def update(self):
        self.x += self.x_speed * self.game.tick * 0.7
        self.y += self.y_speed * self.game.tick * 0.7

        self.collide(self.game.obstacles)

        self.x_speed, self.y_speed = 0, 0


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self, game.sprites, game.mobs)
        self.game = game
        self.image = MOB_IMAGE
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.position = pygame.math.Vector2()
        self.position.x, self.position.y = x, y

        self.velocity = pygame.math.Vector2()
        self.velocity.x, self.velocity.y = 0, 0
        self.acceleration = pygame.math.Vector2()
        self.acceleration.x, self.acceleration.y = 0, 0

        self.rotation = 0
        self.zero_degree_vector = pygame.math.Vector2()
        self.zero_degree_vector.x, self.zero_degree_vector.y = 1, 0

    def avoid(self):
        for mob in self.game.mobs:
            if mob != self:
                shift = self.position - mob.rect.center
                if 0 < shift.length() < max(mob.rect.width, mob.rect.height):
                    self.acceleration += shift.normalize()

    def collide(self, group):
        self.rect.centerx = self.position.x
        hits_list = pygame.sprite.spritecollide(self, group, False, lambda a, b: a.rect.colliderect(b.rect))
        if hits_list:
            if hits_list[0].rect.centerx > self.rect.centerx:
                self.position.x = hits_list[0].rect.left - self.rect.width / 2
            if hits_list[0].rect.centerx < self.rect.centerx:
                self.position.x = hits_list[0].rect.right + self.rect.width / 2
            self.velocity.x = 0
            self.rect.centerx = self.position.x

        self.rect.centery = self.position.y
        hits_list = pygame.sprite.spritecollide(self, group, False, lambda a, b: a.rect.colliderect(b.rect))
        if hits_list:
            if hits_list[0].rect.centery > self.rect.centery:
                self.position.y = hits_list[0].rect.top - self.rect.height / 2
            if hits_list[0].rect.centery < self.rect.centery:
                self.position.y = hits_list[0].rect.bottom + self.rect.height / 2
            self.velocity.y = 0
            self.rect.centery = self.position.y

    def update(self):
        try:
            self.rect.center = self.position

            self.rotation = (self.game.player.rect.topleft - self.position).angle_to(self.zero_degree_vector)

            self.acceleration = self.zero_degree_vector.rotate(-self.rotation)
            self.avoid()
            self.acceleration.scale_to_length(MOB_SPEED)
            self.acceleration -= self.velocity
            self.velocity += self.acceleration * self.game.tick
            self.position += self.velocity * self.game.tick

            self.collide(self.game.obstacles)

        except ValueError:
            pass


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        pygame.sprite.Sprite.__init__(self, game.obstacles)
        self.game = game

        self.rect = pygame.Rect(x, y, width, height)
        self.rect.topleft = x, y


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

    def run(self):
        self.setup()

        running = True
        while running:
            self.clock.tick(FPS)

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

            self.update()

        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()

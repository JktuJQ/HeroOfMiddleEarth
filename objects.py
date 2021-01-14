from constants import *


class Player(pygame.sprite.Sprite):
    """Player class that inherits from pygame.sprite.Sprite"""

    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self, game.sprites, game.players)
        self.image = PLAYER_IMAGE

        self.game = game
        self.target_group = game.mobs

        self.rect = self.image.get_rect()
        self.health_points = PLAYER_HP
        self.draw = 0
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0

        self.inventory = [Weapon('gun', self.target_group, self)]
        self.current_weapon = self.inventory[0]

    def draw_left(self):
        """Animation to left"""
        if self.draw >= 20:
            self.draw = 0
        self.image = LEFT_HERO[self.draw // 5]
        self.draw += 1

    def draw_right(self):
        """Animation to right"""
        if self.draw >= 20:
            self.draw = 0
        self.image = RIGHT_HERO[self.draw // 5]
        self.draw += 1

    def draw_down(self):
        """Animation to down"""
        if self.draw >= 20:
            self.draw = 0
        self.image = DOWN_HERO[self.draw // 5]
        self.draw += 1

    def draw_top(self):
        """Animation to top"""
        if self.draw >= 20:
            self.draw = 0
        self.image = TOP_HERO[self.draw // 5]
        self.draw += 1

    def add_weapon(self, weapon_kind):
        """Adds weapon to player inventory"""
        if len(self.inventory) <= 8 and weapon_kind not in [weapon.kind for weapon in self.inventory]:
            self.inventory.append(Weapon(weapon_kind, self.target_group, self))

    def choose_weapon(self, index):
        """Chooses weapon from inventory"""
        if -1 < index < len(self.inventory):
            self.current_weapon = self.inventory[index]

    def attack(self, pos):
        """Attacks at pos"""
        if self.current_weapon:
            self.current_weapon.attack(pos)

    def get_damage(self, damage):
        """Gets damage and loses health points"""
        self.health_points -= damage
        if self.health_points <= 0:
            self.kill()
            self.game.game.game_over()

    def collide(self, groups):
        """Checks collision"""
        self.rect.x = self.x
        hits_list = pygame.sprite.spritecollide(self, groups, False)
        if hits_list:
            if self.x_speed > 0:
                self.x = hits_list[0].rect.left - self.rect.width
            if self.x_speed < 0:
                self.x = hits_list[0].rect.right
            self.x_speed = 0
            self.rect.x = self.x

        self.rect.y = self.y
        hits_list = pygame.sprite.spritecollide(self, groups, False)
        if hits_list:
            if self.y_speed > 0:
                self.y = hits_list[0].rect.top - self.rect.height
            if self.y_speed < 0:
                self.y = hits_list[0].rect.bottom
            self.y_speed = 0
            self.rect.y = self.y
        if self.game.door.activated and pygame.rect.Rect.colliderect(self.rect, self.game.door):
            if self.game.door.level_index == 3:
                self.get_damage(self.health_points)
            else:
                self.game.game.set_level(self.game.door.level_index)

    def update(self):
        """Updates player stats"""
        if self.x_speed > 0:
            self.x += self.x_speed * self.game.tick * 0.7
            self.draw_right()
        elif self.x_speed < 0:
            self.x += self.x_speed * self.game.tick * 0.7
            self.draw_left()
        if self.y_speed > 0:
            self.y += self.y_speed * self.game.tick * 0.7
            if self.x_speed == 0:
                self.draw_down()
        elif self.y_speed < 0:
            self.y += self.y_speed * self.game.tick * 0.7
            if self.x_speed == 0:
                self.draw_top()
        if self.x_speed == 0 and self.y_speed == 0:
            self.image = PLAYER_IMAGE
        self.current_weapon.cooldown_tracker += self.game.clock.get_time()
        self.collide(self.game.obstacles)

        self.x_speed, self.y_speed = 0, 0


class Weapon:
    """
    Weapon class that implements weapon range, cooldown and damage
    """

    def __init__(self, kind, target_group, player):
        from random import randrange
        self.kind = kind
        self.player = player
        self.target_group = target_group

        self.cooldown = INVENTORY_PROP[kind]['cooldown']
        self.cooldown_tracker = 0

        if type(player) == Mob:
            self.cooldown *= 1.5
            self.cooldown_tracker = randrange(self.cooldown)

    def attack(self, pos):
        """Performs attack with weapon"""
        if self.cooldown_tracker >= self.cooldown:
            Bullet(self.player.rect.x + 15, self.player.rect.y + 15, pos[0], pos[1],
                   self.kind, self, self.target_group)
            self.cooldown_tracker = 0


class Bullet(pygame.sprite.Sprite):
    """
    Bullet class
    """

    def __init__(self, x, y, x1, y1, kind, weapon, target_group):
        import math
        pygame.sprite.Sprite.__init__(self, weapon.player.game.sprites)
        self.style = INVENTORY_PROP[kind]['type of shooting']
        self.dist = INVENTORY_PROP[kind]['range']
        self.damage = INVENTORY_PROP[kind]['damage']
        self.target_group = target_group
        self.y = y
        self.x = x
        self.kind = kind
        self.weapon = weapon
        self.game = weapon.player.game
        self.cam_pos = self.game.camera.camera.topleft
        self.mouse_x = int(x1)
        self.mouse_y = int(y1)
        self.c = 0
        self.speed = 6
        self.being_in_the_list = 0
        if self.style == 'line':
            try:
                self.image = pygame.transform.rotate(INVENTORY_PROP[kind]['animation'],
                                                     self.weapon.player.rotation - 90)
            except Exception:
                self.image = INVENTORY_PROP[kind]['animation']
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect = self.image.get_rect()
            self.side_x = self.mouse_x - self.x
            self.side_y = self.mouse_y - self.y
            self.hyp = math.hypot(self.side_x, self.side_y)
            self.sin = abs(self.side_y) / self.hyp
            self.cos = abs(self.side_x) / self.hyp
            self.degree = math.degrees(math.asin(self.sin))
            if self.hyp != self.dist:
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
        self.update()

    def update(self):
        """Updates bullet"""
        if self.style == 'line':
            try:
                self.rect.x = self.list_of_line_coordinates[self.being_in_the_list][0]
                self.rect.y = self.list_of_line_coordinates[self.being_in_the_list][1]
                self.being_in_the_list += self.speed
                self.collide(self.target_group, self.game.obstacles)

            except IndexError:
                self.kill()

    def collide(self, target_group, collision_group):
        """Checks collision"""
        if pygame.sprite.spritecollide(self, collision_group, False):
            self.kill()
        targets_hits = pygame.sprite.spritecollide(self, target_group, False)
        if targets_hits:
            for target in targets_hits:
                target.get_damage(self.damage)
            self.kill()

    def get_line(self, x1, y1, x2, y2):
        """Gets bullet trajectory"""
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


class Mob(pygame.sprite.Sprite):
    """
    Mob class that inherits from pygame.sprite.Sprite
    """

    def __init__(self, x, y, type, game):
        pygame.sprite.Sprite.__init__(self, game.sprites, game.mobs)
        self.game = game
        self.type = type
        self.target = game.player
        self.image = MOB_IMAGE
        self.health_points = MOB_HP
        self.target_group = game.players
        self.triggered = False

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.position = pygame.math.Vector2()
        self.position.x, self.position.y = x, y
        self.draw = 0

        self.velocity = pygame.math.Vector2()
        self.velocity.x, self.velocity.y = 0, 0
        self.acceleration = pygame.math.Vector2()
        self.acceleration.x, self.acceleration.y = 0, 0

        self.rotation = 0
        self.zero_degree_vector = pygame.math.Vector2()
        self.zero_degree_vector.x, self.zero_degree_vector.y = 1, 0

        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)

        self.inventory = [Weapon(MOBS[type]['type_gun'], self.target_group, self)]
        self.current_weapon = self.inventory[0]

    def add_weapon(self, weapon_kind):
        """Adds weapon to mob"""
        if len(self.inventory) <= 8 and weapon_kind not in [weapon.kind for weapon in self.inventory]:
            self.inventory.append(Weapon(weapon_kind, self.target_group, self))

    def choose_weapon(self, index):
        """Chooses mob's weapon"""
        if -1 < index < len(self.inventory):
            self.current_weapon = self.inventory[index]

    def attack(self, pos):
        """Mob attacks"""
        if self.current_weapon:
            self.current_weapon.attack(pos)

    def get_damage(self, damage):
        """Mob gets damage"""
        self.health_points -= damage
        if self.health_points <= 0:
            self.kill()

    def avoid(self):
        """Avoids being on collision with other mobs"""
        for mob in self.game.mobs:
            if mob != self:
                shift = self.position - mob.rect.center
                if 0 < shift.length() < max(mob.rect.width, mob.rect.height):
                    self.acceleration += shift.normalize()

    def draw_left(self):
        if self.draw >= 20:
            self.draw = 0
        self.image = MOBS[self.type]['animation_l'][self.draw // 10]
        self.draw += 1

    def draw_right(self):
        if self.draw >= 20:
            self.draw = 0
        self.image = MOBS[self.type]['animation_r'][self.draw // 10]
        self.draw += 1

    def collide(self, group):
        """Checks collision"""
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
        """Updates bullet stats"""
        try:
            to_player = self.game.player.rect.topleft - self.position
            if to_player.length() <= 1000:
                self.triggered = True

            if -90 <= self.rotation <= 90:
                self.draw_left()
            else:
                self.draw_right()

            if self.triggered:
                self.rotation = to_player.angle_to(self.zero_degree_vector)

                self.current_weapon.cooldown_tracker += self.clock.get_time()

                self.rect.center = self.position

                self.acceleration = self.zero_degree_vector.rotate(-self.rotation)
                self.avoid()
                self.acceleration.scale_to_length(MOB_SPEED)
                self.acceleration -= self.velocity
                self.velocity += self.acceleration * self.game.tick
                self.position += self.velocity * self.game.tick

                self.collide(self.game.obstacles)
                self.attack(self.game.player.rect.center)
        except ValueError:
            pass


class Obstacle(pygame.sprite.Sprite):
    """
    Obstacle base class
    """

    def __init__(self, x, y, width, height, game):
        pygame.sprite.Sprite.__init__(self, game.obstacles)
        self.game = game

        self.rect = pygame.Rect(x, y, width, height)
        self.rect.topleft = x, y


class Door(pygame.sprite.Sprite):
    """
    Door base class
    """

    def __init__(self, x, y, width, height, index, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.rect = pygame.Rect(x, y, width, height)
        self.rect.topleft = x, y

        self.level_index = int(index)
        self.activated = False

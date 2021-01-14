from map import *
from objects import *
from widgets import *


class Camera:
    """
    Camera class moves all other game objects relative to camera view
    """

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Moves entity relative to camera view"""
        return entity.rect.move(self.camera.topleft)

    def apply_map(self, map):
        """Moves map relative to camera view"""
        return map.move(self.camera.topleft)

    def apply_pos(self, pos):
        """Moves pos relative to camera view"""
        return pos[0] + abs(self.camera.topleft[0]), pos[1] + abs(self.camera.topleft[1])

    def update(self, target):
        """Updates camera rect relative to target"""
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Level:
    """
    Level class which sets all entities, obstacles and sprites on screen
    """

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
        """Loads tiled map from file"""
        self.map = Map(LEVELS[self.index])
        self.full_map = self.map.full_map()
        self.map_rect = self.full_map.get_rect()

    def render(self):
        """Renders all sprites on screen"""
        self.screen.blit(self.full_map, self.camera.apply_map(self.map_rect))
        for sprite in self.sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pygame.display.flip()

    def setup(self):
        """Setups all game objects"""
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
        """Spawns all mobs"""
        for object in self.map.tiled_map_data.objects:
            if object.name == 'Mob':
                Mob(object.x, object.y, object.type, self)


class Game:
    """
    Class which becomes a bridge between widgets and level visualization
    """

    def __init__(self):
        self.paused = False
        self.lost = False

        self.hud_widgets = pygame.sprite.Group()
        self.pause_widgets = pygame.sprite.Group()

    def pause(self):
        """Pauses game"""
        self.paused = True
        pygame.mixer.music.pause()

        self.pause_widgets = pygame.sprite.Group()
        self.pause_menu = LoadingBar(self.current_level.screen, 600, 100, load_data("background_pause_menu.png"),
                                     self.pause_widgets)
        self.paused_label = Label(self.current_level.screen, 710, 130, "Paused!", load_data("title_font.ttf", size=35),
                                  35, self.pause_widgets)
        if not self.lost:
            self.unpause_button = Button(self.current_level.screen, "Continue", 710, 250, self.unpause,
                                         self.pause_widgets,
                                         text_offset=(30, 25))
        self.menu_button = Button(self.current_level.screen, "To menu", 710, 370, self.menu, self.pause_widgets,
                                  text_offset=(30, 25))
        self.exit_button = Button(self.current_level.screen, "Exit", 710, 490, self.terminate, self.pause_widgets,
                                  text_offset=(65, 25))

    def unpause(self):
        """Unpauses game"""
        pygame.mixer.music.unpause()
        self.paused = False

    def menu(self):
        """Starts menu"""
        self.running = False
        self.paused = False
        from screens import Menu
        menu = Menu()
        menu.mainloop()

    def terminate(self):
        """Kills game"""
        self.running = False
        pygame.quit()
        sys.exit(0)

    def setup(self, index):
        """Setups game widgets and level"""
        self.current_level = Level(index, self)

        from random import choice
        pygame.mixer.music.load(os.path.join("data", choice(["game_theme1.mid", "game_theme2.mid"])))
        pygame.mixer.music.play()

        self.background_hp_bar = LoadingBar(self.current_level.screen, 0, 850, load_data("background_hp_bar.png"),
                                            self.hud_widgets)
        self.hp_bar = LoadingBar(self.current_level.screen, 0, 850, load_data("hp_bar.png"), self.hud_widgets,
                                 percent=0.8)
        self.hp_label = Label(self.current_level.screen, 20, 860, "Hp: 200/200", load_data("title_font.ttf", size=20),
                              20,
                              self.hud_widgets)
        self.background_status_label = LoadingBar(self.current_level.screen, 230, 850,
                                                  load_data("background_status_label.png"), self.hud_widgets,
                                                  percent=1)
        self.status_label = Label(self.current_level.screen, 250, 860,
                                  f"Tips: Wave {self.current_level.wave_index + 1} has started",
                                  load_data("title_font.ttf", size=20),
                                  20,
                                  self.hud_widgets)
        self.current_level.setup()

    def update(self):
        """Updates levels, widgets and musics"""
        if self.current_level.wave_index < 1:
            if not self.current_level.mobs.sprites():
                self.current_level.respawn_mobs()
                self.current_level.wave_index += 1
                self.status_label.set_text(f"Tips: Wave {self.current_level.wave_index + 1} has started")
        else:
            self.current_level.door.activated = True
            self.status_label.set_text("Tips: Find portal to other level")
            pygame.mixer.music.fadeout(5000)
        self.current_level.sprites.update()
        self.current_level.camera.update(self.current_level.player)
        self.hp_label.set_text(f"Hp: {self.current_level.player.health_points}/200")
        self.hp_bar.set_percent(self.current_level.player.health_points / 200)
        self.current_level.render()

    def set_level(self, index, player_pos_index=0):
        """Sets level with corresponding index"""
        self.running = False
        self.run(index)

    def game_over(self):
        """Terminates game"""
        self.lost = True
        self.pause()
        self.paused_label.set_text("You lost!")

    def run(self, index):
        """Game mainloop"""
        try:
            self.setup(index)

            self.running = True
            while self.running:
                self.current_level.clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if not self.paused:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == pygame.BUTTON_LEFT:
                                self.current_level.player.attack(self.current_level.camera.apply_pos(event.pos))
                    else:
                        if event.type == pygame.MOUSEMOTION:
                            for widget in self.pause_widgets:
                                widget.update(command="choose", x=event.pos[0], y=event.pos[1])

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == pygame.BUTTON_LEFT:
                                for widget in self.pause_widgets:
                                    widget.update(command="clicked", x=event.pos[0], y=event.pos[1])
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
                    self.pause()
                if not self.paused:
                    self.update()
                    self.hud_widgets.draw(self.current_level.screen)
                if self.paused:
                    self.pause_widgets.draw(self.current_level.screen)
                    try:
                        self.unpause_button.update(command="render_text")
                    except AttributeError:
                        pass
                    self.menu_button.update(command="render_text")
                    self.exit_button.update(command="render_text")
                pygame.display.flip()

            pygame.quit()
        except pygame.error:
            pygame.quit()

from constants import *
from random import randint
from widgets import *
from save import *


class Menu:
    def __init__(self):
        self.running = False

        self.loading = False
        self.loading_percent = 0.1
        self.next = None

        pygame.init()
        pygame.display.set_caption("Hero of MiddleEarth")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        self.background = pygame.transform.scale(load_data("menu_background.gif"), (1600, 900))

        self.labels = pygame.sprite.Group()
        self.label_title = Label(self.screen, 300, 60, "Hero of MiddleEarth",
                                 load_data("title_font.ttf", size=80), 100, self.labels)

        self.buttons = pygame.sprite.Group()
        self.button_play = Button(self.screen, "New game", 50, 600, self.loading_play, self.buttons, text_offset=(20, 25))
        self.button_play = Button(self.screen, "Load game", 50, 700, self.loading_load, self.buttons, text_offset=(15, 25))
        self.button_exit = Button(self.screen, "Exit", 50, 800, self.terminate, self.buttons, text_offset=(65, 25))

        self.loading_widgets = pygame.sprite.Group()
        self.loading_bar = LoadingBar(self.screen, 1100, 800, load_data("loading_bar.png"),
                                      self.loading_widgets, percent=self.loading_percent)
        self.loading_label = Label(self.screen, 1100, 700, "Loading...", load_data("title_font.ttf", size=50), 50,
                                   self.loading_widgets, font_color=pygame.color.Color("red"))

    def start_loading(self, next):
        self.loading = True
        self.next = next

    def loading_play(self):
        self.start_loading(next=self.play)

    def loading_load(self):
        self.start_loading(next=self.load)

    def play(self):
        self.running = False
        self.loading = False
        pygame.quit()
        from level import Game
        game = Game()
        save_data("game.level", 0, os.path.join("saves", "save"))
        game.run(get_data("game.level", os.path.join("saves", "save")))

    def load(self):
        self.running = False
        self.loading = False
        pygame.quit()
        from level import Game
        game = Game()
        game.run(get_data("game.level", os.path.join("saves", "save")))

    def terminate(self):
        self.running = False
        self.loading = False
        pygame.quit()
        sys.exit(0)

    def mainloop(self):
        self.running = True

        try:
            while self.running:
                self.screen.blit(self.background, self.background.get_rect())
                if not self.loading:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.terminate()

                        elif event.type == pygame.MOUSEMOTION:
                            for button in self.buttons:
                                button.update(command="choose", x=event.pos[0], y=event.pos[1])

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                for button in self.buttons:
                                    button.update(command="clicked", x=event.pos[0], y=event.pos[1])
                    self.labels.draw(self.screen)
                    self.buttons.draw(self.screen)
                    for button in self.buttons:
                        button.update(command="render_text")
                    pygame.display.flip()
                else:
                    self.loading_widgets.draw(self.screen)
                    self.loading_percent += (0.1 if randint(0, 200) == 0 else 0)
                    self.loading_bar.set_percent(self.loading_percent)
                    if self.loading_percent >= 1:
                        self.next()
                    pygame.display.flip()
        except pygame.error:
            pass

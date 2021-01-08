from constants import *
import shelve
import typing


# Functions
def load_data(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    ext = fullname.split(".")[-1].lower()
    file = None
    if ext == "png" or ext == "jpg":  # Load image
        file = pygame.image.load(fullname)
    elif ext == "ttf":  # Load font
        file = pygame.font.Font(name, 25)
    return file  # If file is None, then file extension is unknown


# Classes
class Label(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface, x: int, y: int, text: str, font_name: str, font_size: int,
                 *groups,
                 font_color: pygame.Color = pygame.Color("black")):

        super().__init__(*groups)

        self.screen = screen

        self.label_text = load_data(pygame.font.match_font(font_name)).render(text, True, font_color)
        self.label_rect = self.label_text.get_rect()

    def move_on(self, offset_x: int, offset_y: int):
        self.label_rect.x, self.label_rect.y = self.label_rect.x + offset_x, self.label_rect.y + offset_y

    def move_to(self, x: int, y: int):
        self.label_rect.x, self.label_rect.y = x, y

    def update(self):
        self.screen.blit(self.label_text, self.label_rect)


class Button(pygame.sprite.Sprite):

    image = load_data("button_texture.png")

    def __init__(self, screen: pygame.Surface, text: str, x: int, y: int, binded_function,
                 *groups,
                 text_offset: typing.Tuple[int, int] = (50, 25)):
        super().__init__(*groups)

        self.screen = screen

        self.chosen = False
        self.binded_function = binded_function
        self.text_offset = text_offset

        self.texture = Button.image
        self.rect = self.texture.get_rect()

        self.label = Label(screen, x, y, text, "magneto", 25)

        self.move_to(x, y)

    def move_on(self, offset_x: int, offset_y: int):
        self.rect.x, self.rect.y = self.rect.x + offset_x, self.rect.y + offset_y
        self.label.move_on(offset_x, offset_y)

    def move_to(self, x: int, y: int):
        self.rect.x, self.rect.y = x, y
        self.label.move_to(x, y)
        self.label.move_on(self.text_offset[0], self.text_offset[1])

    def choose(self):
        if not self.chosen:
            self.chosen = not self.chosen
            self.move_on(0, -10)

    def unchoose(self):
        if self.chosen:
            self.chosen = not self.chosen
            self.move_on(0, 10)

    def clicked(self):
        self.binded_function()

    def on_click(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and \
                y in range(self.rect.y, self.rect.y + self.rect.height):
            return True
        return False

    def update(self, *args, command: str = "", **kwargs) -> None:
        if command == "move":
            self.move_to(kwargs["x"], kwargs["y"])
        elif command == "choose":
            if self.on_click(kwargs["x"], kwargs["y"]):
                self.choose()
            else:
                self.unchoose()
        elif command == "clicked":
            if self.on_click(kwargs["x"], kwargs["y"]):
                self.clicked()
        elif command == "render_text":
            self.label.update()


class LoadingBar(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, x: int, y: int, image: pygame.Surface,
                 *groups,
                 percent: float = 1):
        super().__init__(*groups)

        self.screen = screen

        self.image = image
        self.rect = self.image.get_rect()

        self.set_percent(percent)

        self.move_to(x, y)

    def move_on(self, offset_x: int, offset_y: int):
        self.rect.x, self.rect.y = self.rect.x + offset_x, self.rect.y + offset_y

    def move_to(self, x: int, y: int):
        self.rect.x, self.rect.y = x, y

    def set_percent(self, percent: float):
        self.image = pygame.transform.scale(self.image, (round(self.rect.width * percent), self.rect.height))
        self.rect = self.image.get_rect()

    def update(self, *args, command: str = "", **kwargs):
        self.screen.blit(self.image, self.rect)


def game(data):
    print(data)


def terminate():
    pygame.quit()
    sys.exit(0)


def play():
    with shelve.open(os.path.join("saves", "save1")) as savedata:
        savedata["hero.hp"] = 5
        savedata["hero.function"] = game


def load():
    data = dict()
    with shelve.open(os.path.join("saves", "save1")) as savedata:
        for key in savedata.keys():
            data[key] = savedata[key]
    game(data)



WINDOW_SIZE = WIDTH, HEIGHT = 1600, 900
pygame.init()
pygame.display.set_caption("Hero of MiddleEarth")
screen = pygame.display.set_mode(WINDOW_SIZE)


def main():
    bars = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    health_bar = LoadingBar(screen, 100, 100, load_data("button_texture.png"), bars)
    button_play = Button(screen, "New game", 50, 600, play, buttons, text_offset=(20, 25))
    button_play = Button(screen, "Load game", 50, 700, load, buttons, text_offset=(15, 25))
    button_exit = Button(screen, "Exit", 50, 800, terminate, buttons, text_offset=(65, 25))

    running = True
    while running:
        screen.fill(pygame.Color("white"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.MOUSEMOTION:
                buttons.update(command="choose", x=event.pos[0], y=event.pos[1])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(command="clicked", x=event.pos[0], y=event.pos[1])

        buttons.draw(screen)
        buttons.update(command="render_text")
        bars.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
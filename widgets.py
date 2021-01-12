from constants import *
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

    def __init__(self, screen: pygame.Surface, x: int, y: int, text: str, font: pygame.font.Font, font_size: int,
                 *groups,
                 font_color: pygame.Color = pygame.Color("black")):

        super().__init__(*groups)

        self.screen = screen

        self.image = font.render(text, True, font_color)
        self.rect = self.image.get_rect()

        self.move_to(x, y)

    def move_on(self, offset_x: int, offset_y: int):
        self.rect.x, self.rect.y = self.rect.x + offset_x, self.rect.y + offset_y

    def move_to(self, x: int, y: int):
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.screen.blit(self.image, self.rect)


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

        self.label = Label(screen, x, y, text, pygame.font.SysFont("magneto", 25), 25, font_color=pygame.color.Color("white"))

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

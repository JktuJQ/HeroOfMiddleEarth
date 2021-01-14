from constants import *
import typing


# Classes
class Label(pygame.sprite.Sprite):
    """
    Label widgets that displays text
    """

    def __init__(self, screen: pygame.Surface, x: int, y: int, text: str, font: pygame.font.Font, font_size: int,
                 *groups,
                 font_color: pygame.Color = pygame.Color("black")):
        super().__init__(*groups)

        self.screen = screen

        self.font = font
        self.font_color = font_color

        self.set_text(text)
        self.rect = self.image.get_rect()

        self.move_to(x, y)

    def move_on(self, offset_x: int, offset_y: int):
        """Moves label on vector"""
        self.rect.x, self.rect.y = self.rect.x + offset_x, self.rect.y + offset_y

    def move_to(self, x: int, y: int):
        """Moves label to x, y pos"""
        self.rect.x, self.rect.y = x, y

    def set_text(self, text: str):
        """Sets new text to label"""
        self.image = self.font.render(text, True, self.font_color)
        self.image.set_colorkey(pygame.color.Color("white"))

    def update(self, *args, **kwargs):
        """Renders itself on screen"""
        self.screen.blit(self.image, self.rect)


class Button(pygame.sprite.Sprite):
    """
    Button widgets that is used to call function when button is pressed
    """

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

        self.label = Label(self.screen, x, y, text, load_data("magneto_font.ttf", size=25), 25,
                           font_color=pygame.color.Color("black"))

        self.move_to(x, y)

    def move_on(self, offset_x: int, offset_y: int):
        """Moves label on vector"""
        self.rect.x, self.rect.y = self.rect.x + offset_x, self.rect.y + offset_y
        self.label.move_on(offset_x, offset_y)

    def move_to(self, x: int, y: int):
        """Moves label to x, y pos"""
        self.rect.x, self.rect.y = x, y
        self.label.move_to(x, y)
        self.label.move_on(self.text_offset[0], self.text_offset[1])

    def choose(self):
        """Selects button"""
        if not self.chosen:
            self.chosen = not self.chosen
            self.move_on(0, -10)

    def unchoose(self):
        """Unselects button"""
        if self.chosen:
            self.chosen = not self.chosen
            self.move_on(0, 10)

    def clicked(self):
        """Calls function when clicked"""
        self.binded_function()

    def on_click(self, x, y):
        """Checks is on click"""
        if x in range(self.rect.x, self.rect.x + self.rect.width) and \
                y in range(self.rect.y, self.rect.y + self.rect.height):
            return True
        return False

    def update(self, *args, command: str = "", **kwargs) -> None:
        """Updates itself with calling functions"""
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
    """
    LoadingBar widget which shows image that can be scaled on percent
    """

    def __init__(self, screen: pygame.Surface, x: int, y: int, image: pygame.Surface,
                 *groups,
                 percent: float = 1):
        super().__init__(*groups)

        self.screen = screen

        self.source_image = image
        self.image = self.source_image.copy()
        self.rect = self.source_image.get_rect()

        self.set_percent(percent)

        self.move_to(x, y)

    def move_on(self, offset_x: int, offset_y: int):
        """Moves loadingbar on vector"""
        self.rect.x, self.rect.y = self.rect.x + offset_x, self.rect.y + offset_y

    def move_to(self, x: int, y: int):
        """Moves loadingbar to x, y pos"""
        self.rect.x, self.rect.y = x, y

    def set_percent(self, percent: float):
        """Sets percent to loading bar"""
        self.image = pygame.transform.scale(self.source_image.copy(),
                                            (round(self.rect.width * percent), self.rect.height))

    def update(self, *args, command: str = "", **kwargs):
        """Renders itself on screen"""
        self.screen.blit(self.image, self.rect)

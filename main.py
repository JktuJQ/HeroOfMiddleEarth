from widgets import *
from save import *


# Global
running = True


# Functions
def load_data(name, **kwargs):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    ext = fullname.split(".")[-1].lower()
    file = None
    if ext == "png" or ext == "jpg" or ext == "gif":  # Load image
        file = pygame.image.load(fullname)
    elif ext == "ttf":  # Load font
        try:
            file = pygame.font.Font(name, kwargs.get("size"))
        except FileNotFoundError:
            file = pygame.font.Font(fullname, kwargs.get("size"))
    return file  # If file is None, then file extension is unknown


def terminate():
    global running
    running = False
    pygame.quit()
    sys.exit(0)


def play():
    global running
    running = False
    pygame.quit()
    from level import Game
    game = Game()
    save_data("game.level", 0, os.path.join("saves", "save"))
    game.run(get_data("game.level", os.path.join("saves", "save")))


def load():
    global running
    running = False
    pygame.quit()
    from level import Game
    game = Game()
    game.run(get_data("game.level", os.path.join("saves", "save")))


WINDOW_SIZE = WIDTH, HEIGHT = 1600, 900
pygame.init()
pygame.display.set_caption("Hero of MiddleEarth")
screen = pygame.display.set_mode(WINDOW_SIZE)


def main():
    background = pygame.transform.scale(load_data("menu_background.gif"), (1600, 900))

    labels = pygame.sprite.Group()
    label_title = Label(screen, 300, 60, "Hero of MiddleEarth", load_data("title_font.ttf", size=80), 100, labels)

    buttons = pygame.sprite.Group()
    button_play = Button(screen, "New game", 50, 600, play, buttons, text_offset=(20, 25))
    button_play = Button(screen, "Load game", 50, 700, load, buttons, text_offset=(15, 25))
    button_exit = Button(screen, "Exit", 50, 800, terminate, buttons, text_offset=(65, 25))

    while running:
        screen.fill(pygame.Color("white"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.MOUSEMOTION:
                buttons.update(command="choose", x=event.pos[0], y=event.pos[1])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons.update(command="clicked", x=event.pos[0], y=event.pos[1])
        try:
            screen.blit(background, background.get_rect())
            labels.draw(screen)
            buttons.draw(screen)
            buttons.update(command="render_text")
            pygame.display.flip()
        except pygame.error:
            pass


if __name__ == "__main__":
    main()

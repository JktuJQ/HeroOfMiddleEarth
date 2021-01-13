from constants import *
from screens import *


pygame.init()
pygame.display.set_caption("Hero of MiddleEarth")
screen = pygame.display.set_mode(WINDOW_SIZE)


def main():
    menu = Menu()
    menu.mainloop()


if __name__ == "__main__":
    main()

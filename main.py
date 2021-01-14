from screens import *

pygame.init()
pygame.display.set_caption("Hero of MiddleEarth")
pygame.display.set_icon(pygame.image.load('data/images/icon.jpg'))
screen = pygame.display.set_mode(WINDOW_SIZE)


def main():
    menu = Menu()
    menu.mainloop()


if __name__ == "__main__":
    main()

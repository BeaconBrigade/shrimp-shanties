import pygame

from shrimp_shanties.front_page import FrontPage

WIDTH = 1000
HEIGHT = 600


def main():
    global WIDTH, HEIGHT

    pygame.init()
    screen = pygame.display.set_mode(size=[WIDTH, HEIGHT], flags=pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Shrimp Shanties")

    state = FrontPage()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH = event.w, HEIGHT = event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        state.update(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()

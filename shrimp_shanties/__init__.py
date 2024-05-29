import pygame
import pygame_gui

from shrimp_shanties.asset_manager import AssetManager

WIDTH = 1000
HEIGHT = 600

from shrimp_shanties.menu.front_page import FrontPage
from shrimp_shanties.state import State


def main():
    global WIDTH, HEIGHT

    pygame.init()

    screen = pygame.display.set_mode(size=[WIDTH, HEIGHT], flags=pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Shrimp Shanties")

    manager = pygame_gui.UIManager((WIDTH, HEIGHT), AssetManager.load_theme('base.json'))

    game_state = State()
    State.BASE = game_state
    State.MANAGER = manager
    game_state.push(FrontPage())

    running = True
    while running:
        delta = clock.tick(60)/1000.
        fps = 1 / delta
        #print('\033[2J\033[H', end='')
        print(f'{fps:2} fps ({delta})')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH = event.w
                HEIGHT = event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                manager.set_window_resolution((WIDTH, HEIGHT))

            manager.process_events(event)
            game_state.propagate_event(event)

        manager.update(delta)
        game_state.update(delta)

        game_state.propagate_draw(screen)
        manager.draw_ui(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()

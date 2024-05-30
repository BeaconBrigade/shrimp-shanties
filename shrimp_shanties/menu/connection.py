import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements import UILabel, UIButton, UIDropDownMenu

from shrimp_shanties import AssetManager
from shrimp_shanties.state import State
from shrimp_shanties.game import Game
from shrimp_shanties.menu.marketplace import Marketplace


class Connection(State):
    def __init__(self):
        super().__init__()

        self.ui_elements.append(UILabel(relative_rect=pygame.Rect((0, 20), (-1, -1)), object_id="@subheading",
                                        text="Connect with other players", anchors={'centerx': 'centerx', 'top': 'top'},
                                        manager=State.MANAGER))

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((0, 0), (-1, -1)), object_id="#start-game", text="Connect",
                     anchors={'center': 'center'}, manager=State.MANAGER))

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((0, 70), (-1, -1)), object_id="#start-shop", text="Marketplace",
                     anchors={'center': 'center'}, manager=State.MANAGER))

        available_shanties = AssetManager.list_shanties()
        print(available_shanties)
        menu = UIDropDownMenu(relative_rect=pygame.Rect((0, 140), (200, 50)), object_id="#select-theme",
                              starting_option=available_shanties[0], options_list=available_shanties,
                              anchors={'center': 'center'}, manager=State.MANAGER)
        self.ui_elements.append(menu)

    def draw(self, screen: Surface):
        screen.fill((30, 30, 50))

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[1]:
            # TODO: actually connect to other players
            pygame.event.clear()
            self.push(Game(self.ui_elements[-1].selected_option))
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[2]:
            pygame.event.clear()
            self.push(Marketplace())
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.get_parent().pop()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.event.clear()
            self.push(Game(self.ui_elements[-1].selected_option))

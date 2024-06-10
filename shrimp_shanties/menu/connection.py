import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements import UILabel, UIButton, UIDropDownMenu

from shrimp_shanties import AssetManager
from shrimp_shanties.game.startup import Startup
from shrimp_shanties.menu.marketplace import Marketplace
from shrimp_shanties.shanty import Shanty
from shrimp_shanties.state import State


class Connection(State):
    def __init__(self):
        super().__init__()

        self.ui_elements.append(UILabel(relative_rect=pygame.Rect((0, 20), (-1, -1)), object_id="@subheading",
                                        text="Launch Pad", anchors={'centerx': 'centerx', 'top': 'top'},
                                        manager=State.MANAGER))

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((-70, 140), (-1, -1)), object_id="#start-game", text="Online",
                     anchors={'centerx': 'centerx', 'top': 'top'}, manager=State.MANAGER))
        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((70, 140), (-1, -1)), object_id="#start-game", text="Offline",
                     anchors={'centerx': 'centerx', 'top': 'top'}, manager=State.MANAGER))

        self.ui_elements.append(
            UIButton(relative_rect=pygame.Rect((0, 280), (-1, -1)), object_id="#start-shop", text="Marketplace",
                     anchors={'centerx': 'centerx', 'top': 'top'}, manager=State.MANAGER))

        self.available_shanties = AssetManager.list_shanties()
        lengths = [Shanty(n).length() // 60 for n in self.available_shanties]
        self.available_shanty_str = [f"{n} ({(l // 60) // 60}:{(l // 60) % 60:02}:{l % 60:02})" for n, l
                                in zip(self.available_shanties, lengths)]

        print(self.available_shanties)
        menu = UIDropDownMenu(relative_rect=pygame.Rect((0, 70), (400, 50)), object_id="#select-theme",
                              starting_option=self.available_shanty_str[0], options_list=self.available_shanty_str,
                              anchors={'centerx': 'centerx', 'top': 'top'}, manager=State.MANAGER)
        self.ui_elements.append(menu)

    def draw(self, screen: Surface):
        screen.fill((30, 30, 50))

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[1]:
            pygame.event.clear()
            # TODO: actually connect to other players
            print("Multiplayer connectivity not currently supported.")
            selected = self.ui_elements[-1].selected_option
            idx = self.available_shanty_str.index(selected)
            self.push(Startup(self.available_shanties[idx]))
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[2]:
            pygame.event.clear()
            selected = self.ui_elements[-1].selected_option
            idx = self.available_shanty_str.index(selected)
            self.push(Startup(self.available_shanties[idx]))
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_elements[3]:
            pygame.event.clear()
            self.push(Marketplace())
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            click = AssetManager.load_sound("button-click.wav")
            click.play()
            self.get_parent().pop()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # not playing sound here as it overlaps with the Startup beeps
            pygame.event.clear()
            selected = self.ui_elements[-1].selected_option
            idx = self.available_shanty_str.index(selected)
            self.push(Startup(self.available_shanties[idx]))

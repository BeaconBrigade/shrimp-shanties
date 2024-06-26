import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements import UIPanel, UILabel, UIButton, UIImage

from ..menu.marketplace import Marketplace
from .. import HEIGHT
from .. import AssetManager
from ..state import State


class Over(State):
    def __init__(self, score, misses, percent):
        super().__init__()
        self.score = score
        self.misses = misses
        self.percent = percent

        panel = UIPanel(relative_rect=pygame.Rect((0, 0), (400, HEIGHT*0.9)), anchors={'centerx': 'centerx', 'centery': 'centery'},
                        object_id="#pause-panel", manager=State.MANAGER)
        self.ui_elements.append(panel)

        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, 20), (-1, -1)), container=panel,
                    anchors={'centerx': 'centerx', 'top': 'top'}, text='Game Over', object_id='@subheading',
                    manager=State.MANAGER)
        )

        percent = round(self.percent, 2)
        end_sound = AssetManager.load_sound("sectionpass.mp3")
        if percent < 50:
            end_sound = AssetManager.load_sound("sectionfail.mp3")
            letter = 'F'
        elif percent < 70:
            letter = 'D'
        elif percent < 80:
            letter = 'C'
        elif percent < 90:
            letter = 'B'
        elif percent < 100:
            letter = 'A'
        elif percent == 100:
            letter = 'S'
        else:
            raise Exception("you are dumb")
        end_sound.play()
        if percent == 100:
            # Display the image separately
            image = AssetManager.load_texture('s.png')
            self.ui_elements.append(
                UIImage(relative_rect=pygame.Rect((0, 180), (image.get_width()/2, image.get_height()/2)),
                        container=panel, anchors={'centerx': 'centerx', 'top': 'top'},
                        image_surface=image, manager=State.MANAGER)
            )  
            self.ui_elements.append(
                UILabel(relative_rect=pygame.Rect((0, 240), (-1, -1)), container=panel,
                        anchors={'centerx': 'centerx', 'top': 'top'},
                        text=f'{percent}%', object_id='#start-game',
                        manager=State.MANAGER)
            ) 
        else:
            # Display the text with the letter grade
            self.ui_elements.append(
                UILabel(relative_rect=pygame.Rect((0, 240), (-1, -1)), container=panel,
                        anchors={'centerx': 'centerx', 'top': 'top'},
                        text=f'{percent}% ({letter})', object_id='#start-game',
                        manager=State.MANAGER)
            )

        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, 290), (-1, -1)), container=panel,
                    anchors={'centerx': 'centerx', 'top': 'top'},
                    text=f'You scored {self.score} points!', object_id='#start-game',
                    manager=State.MANAGER)
        )

        self.ui_elements.append(
            UILabel(relative_rect=pygame.Rect((0, 360), (-1, -1)), container=panel,
                    anchors={'centerx': 'centerx', 'top': 'top'},
                    text=f'{self.misses} misses', object_id='#start-game',
                    manager=State.MANAGER)
        )

        self.market = UIButton(relative_rect=pygame.Rect((0, -140), (-1, -1)), container=panel,
                               anchors={'center': 'center'}, text="Marketplace", object_id='#start-game',
                               manager=State.MANAGER)
        self.ui_elements.append(self.market)

        self.launch = UIButton(relative_rect=pygame.Rect((-1, -100), (-1, -1)), container=panel,
                               anchors={'centerx': 'centerx', 'bottom': 'bottom'}, text="Launch Pad",
                               object_id='#start-game')
        self.ui_elements.append(self.launch)

    def draw(self, screen: Surface):
        parent_surface = pygame.Surface(screen.get_size())
        parent_surface.set_alpha(255)
        self.get_parent().draw(parent_surface)

        shaded_surface = pygame.Surface(screen.get_size())
        shaded_surface.fill((0, 0, 0))
        shaded_surface.set_alpha(128)
        parent_surface.blit(shaded_surface, (0, 0))

        screen.blit(parent_surface, (0, 0))

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.market:
            self.get_parent().push(Marketplace())
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.launch:
            front = self.get_parent().get_parent()
            front.get_parent().start_menu_music()
            front.pop()
            front.pop()

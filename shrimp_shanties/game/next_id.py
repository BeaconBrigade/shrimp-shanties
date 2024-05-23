import pygame

START_ID = 100
__entity_count = 0


def next_entity_id() -> int:
    """ Generate the next entity id """
    global __entity_count
    __entity_count += 1
    return START_ID + __entity_count


def next_event_id() -> int:
    """ Generate the next event id """
    return pygame.event.custom_type()

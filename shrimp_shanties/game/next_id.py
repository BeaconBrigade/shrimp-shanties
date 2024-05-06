import pygame

START_ID = 100
__entity_count = 0
__event_count = 0


def next_entity_id() -> int:
    """ Generate the next entity id """
    global __entity_count
    __entity_count += 1
    return START_ID + __entity_count


def next_event_id() -> int:
    """ Generate the next event id """
    global __event_count
    __event_count += 1
    return pygame.USEREVENT + __event_count

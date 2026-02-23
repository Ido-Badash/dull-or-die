import pygame


class TriggerHandler:
    @staticmethod
    def trigger_single_key(events, key: int):
        return any(e.type == pygame.KEYDOWN and e.key == key for e in events)

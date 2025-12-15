# camera.py
import pygame
import random
from core.settings import *

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.shake_offset = pygame.Vector2(0, 0)

        self.shake_time = 0
        self.shake_duration = 0
        self.shake_intensity = 0

    def update(self, player, dt):
        # follow player
        self.offset.x = player.rect.centerx - SCREEN_W // 2
        self.offset.y = player.rect.centery - SCREEN_H // 2

        # update shake
        if self.shake_time > 0:
            self.shake_time -= dt
            self.shake_offset.x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset.y = random.randint(-self.shake_intensity, self.shake_intensity)
        else:
            self.shake_offset.update(0, 0)

    def shake(self, intensity=6, duration=0.25):
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_time = duration

    def apply(self, rect):
        return rect.move(
            -self.offset.x + self.shake_offset.x,
            -self.offset.y + self.shake_offset.y
        )

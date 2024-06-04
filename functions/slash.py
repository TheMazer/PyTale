import pygame

from settings import *

from functions.import_folder import importFolder


class Slash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = importFolder('assets/images/slash')
        self.animationSpeed = 0.2
        self.frameIndex = 0
        self.done = False

        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.topleft = (screenSize[0] / 2 - self.image.get_width() / 2, 100)

    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.image = pygame.Surface((0, 0))
            self.done = True
        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.animate()

    def reset(self):
        self.frameIndex = 0
        self.done = False

        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.topleft = (screenSize[0] / 2 - self.image.get_width() / 2, 100)
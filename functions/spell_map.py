import pygame

from settings import *


class SpellMap:
    def __init__(self, battleClass):
        self.battleClass = battleClass
        self.resizingSpeed = 4
        self.width = 0
        self.height = 0
        self.rect = pygame.Rect(321 - self.width / 2, 281 - self.height / 2, self.width, self.height)

    def resizing(self):
        mapSize = self.battleClass.mapSize
        if mapSize[0] > self.width:
            self.width += (mapSize[0] - self.width) / self.resizingSpeed
        elif mapSize[0] < self.width:
            self.width += (mapSize[0] - self.width) / self.resizingSpeed

        if mapSize[1] > self.height:
            self.height += (mapSize[1] - self.height) / self.resizingSpeed
        elif mapSize[1] < self.height:
            self.height += (mapSize[1] - self.height) / self.resizingSpeed

        self.x = 0

    def update(self):
        self.resizing()

    def draw(self, displaySurface):
        self.rect = pygame.Rect(321 - self.width / 2, 281 - self.height / 2, self.width, self.height)
        pygame.draw.rect(displaySurface, 'White', self.rect, 5)
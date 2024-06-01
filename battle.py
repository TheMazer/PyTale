import random

import pygame

from settings import *

from player import Soul
from functions.spell_map import SpellMap
from functions.button import Button


class Battle:
    def __init__(self):
        # Setup
        self.displaySurface = pygame.display.get_surface()
        self.mapSize = (165, 165)

        # PLayer
        self.spellMap = SpellMap(self)
        self.soul = Soul(self)
        self.lv = 19
        self.hp = 48
        self.maxHp = 92

        # Gui
        self.name = statusFont.render('Chara', False, 'White')
        self.lvLabel = statusFont.render('LV ' + str(self.lv), False, 'White')
        self.hpLabel = statusFont.render(str(self.hp) + ' / ' + str(self.maxHp), False, 'White')

        self.hpTip = tipFont.render('HP', False, 'White')

        self.buttons = {Button('fight', 0), Button('act', 1), Button('item', 2), Button('mercy', 3)}

    def run(self, dt):
        self.displaySurface.fill('Black')

        # Spell Map Processing
        self.spellMap.update()
        self.spellMap.draw(self.displaySurface)

        # Gui
        self.displaySurface.blit(self.name, (32, 380))
        self.displaySurface.blit(self.lvLabel, (134, 380))
        self.displaySurface.blit(self.hpLabel, (296 + (self.maxHp - 20) * 1.2, 380))

        self.displaySurface.blit(self.hpTip, (226, 384))
        pygame.draw.rect(self.displaySurface, '#BF0000', (256, 380, self.maxHp * 1.2, 21))
        pygame.draw.rect(self.displaySurface, '#FFFF00', (256, 380, self.hp * 1.2, 21))

        for button in self.buttons:
            self.displaySurface.blit(button.image, button.rect)

        # Soul Processing
        self.soul.update()
        self.displaySurface.blit(self.soul.image, self.soul.rect)
        # pygame.draw.rect(self.displaySurface, 'Yellow', self.soul.hitbox)

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_f]:
            self.mapSize = (random.randint(50, 600), random.randint(50, 400))
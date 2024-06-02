import pygame

from settings import *
import random

from player import Soul
from enemy import Pyhtoncheg
from functions.spell_map import SpellMap
from functions.button import Button
from functions.font_processor import DialogueFont, OptionFont


class Battle:
    def __init__(self):
        # Setup
        self.displaySurface = pygame.display.get_surface()
        self.menuEnabled = False
        self.mapSize = (165, 165)

        # PLayer
        self.spellMap = SpellMap(self)
        self.soul = Soul(self)
        self.lv = 19
        self.hp = 48
        self.maxHp = 92

        # Enemy
        self.enemy = Pyhtoncheg(self)
        self.enemySelect = [OptionFont(self.enemy.name)]  # Name of one enemy by now
        self.acts = [OptionFont(option) for option in self.enemy.acts]
        self.acts.insert(0, OptionFont('Проверить'))

        # Gui
        self.name = statusFont.render('Chara', False, 'White')
        self.lvLabel = statusFont.render('LV ' + str(self.lv), False, 'White')
        self.hpLabel = statusFont.render(str(self.hp) + ' / ' + str(self.maxHp), False, 'White')
        self.hpTip = tipFont.render('HP', False, 'White')
        self.buttons = [Button('fight', 0), Button('act', 1), Button('item', 2), Button('mercy', 3)]

        # Navigation
        self.selected = 0  # Buttons
        self.optionSelect = 0  # Options in menus
        self.cooldown = 0  # Cooldown Before Enters
        self.inMenu = False  # Button Pressed
        self.messageSent = False  # Status message in progress
        self.enemySelected = None  # Selected Enemy (for Fight, Act menu)
        self.buttons[self.selected].hover(1)

        # Music
        self.theme = pygame.mixer.Sound('assets/music/Megalo_Strike_Back.ogg')
        self.theme.set_volume(.3)
        self.theme.play(loops=-1)

        # Sounds
        self.menuMoveSound = pygame.mixer.Sound('assets/sounds/menu_move.wav')
        self.selectSound = pygame.mixer.Sound('assets/sounds/select.wav')

        self.enableMenu()

    def enableMenu(self):
        self.menuEnabled = True
        self.mapSize = (575, 140)
        if self.enemy.firstStatusMessages: statusMessage = self.enemy.firstStatusMessages
        else: statusMessage = [self.enemy.name + ' приближается.']
        self.menuDialogue = DialogueFont(*statusMessage)
        self.buttons[self.selected].hover(1)

    def enemyTurn(self):
        self.inMenu = False
        self.menuEnabled = False
        self.messageSent = False
        self.enemySelected = None
        self.mapSize = (165, 140)
        self.buttons[self.selected].hover(0)

    def sendMessage(self, *type):
        self.menuDialogue = DialogueFont(*type)
        self.messageSent = True

    def menuProcessing(self):
        self.getInput()
        if not self.inMenu:
            self.menuDialogue.render(self.displaySurface, (56, 254))
            self.displaySurface.blit(self.soul.image, self.buttons[self.selected].rect.topleft + pygame.Vector2(8, 13))
        elif self.messageSent:
            self.menuDialogue.render(self.displaySurface, (56, 254))
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_RETURN] and self.menuDialogue.done:
                self.enemyTurn()
            elif keys[pygame.K_x]:
                self.menuDialogue.done = True
                for i in range(len(self.menuDialogue.printingPos)):
                    self.menuDialogue.printingPos[i] = 100
        elif self.selected == 1:
            if self.enemySelected is None:
                self.enemySelection()
            else:
                self.optionSelection()
                for index, option in enumerate(self.acts):
                    option.render(self.displaySurface, (96 + index % 2 * 230, 254 + index // 2 * 32))

    def enemySelection(self):
        self.displaySurface.blit(self.soul.image, pygame.Vector2(96, 254) + pygame.Vector2(-32, 4))
        for index, enemy in enumerate(self.enemySelect):
            enemy.render(self.displaySurface, (96, 254 + index * 24))

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_RETURN] and not self.cooldown:
            self.enemySelected = self.enemy.name  # Name of one enemy by now
            self.selectSound.play()
            self.cooldown = 5

    def optionSelection(self):
        self.displaySurface.blit(self.soul.image, pygame.Vector2(96 + self.optionSelect % 2 * 230, 254 + self.optionSelect // 2 * 32) + pygame.Vector2(-32, 4))
        lastSelected = self.optionSelect

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_RETURN] and not self.cooldown:
            print('Selected:', self.acts[self.optionSelect].value)
            self.enemy.act(self.acts[self.optionSelect].value)
            self.cooldown = 5
        elif keys[pygame.K_a]:
            self.optionSelect = max(self.optionSelect - 1, 0)
        elif keys[pygame.K_d]:
            self.optionSelect = min(self.optionSelect + 1, len(self.acts) - 1)
        elif keys[pygame.K_w]:
            self.optionSelect = max(self.optionSelect - 2, 0)
        elif keys[pygame.K_s]:
            self.optionSelect = min(self.optionSelect + 2, len(self.acts) - 1)

        if lastSelected != self.optionSelect:
            self.selectSound.play()

    def buttonHoverEffect(self, index):
        [button.hover(0) for button in self.buttons]
        self.buttons[index].hover(1)

    def getInput(self):
        keys = pygame.key.get_just_pressed()
        if not self.inMenu:
            if keys[pygame.K_RETURN] and not self.cooldown:
                self.selectSound.play()
                self.inMenu = True
                self.cooldown = 5
            elif keys[pygame.K_a]:
                self.selected = 3 if self.selected == 0 else self.selected - 1
                self.buttonHoverEffect(self.selected)
                self.menuMoveSound.play()
            elif keys[pygame.K_d]:
                self.selected = 0 if self.selected == 3 else self.selected + 1
                self.buttonHoverEffect(self.selected)
                self.menuMoveSound.play()
        elif not self.enemySelected:
            if keys[pygame.K_x]:
                for i in range(len(self.menuDialogue.printingPos)):
                    self.menuDialogue.printingPos[i] = 0
                self.selectSound.play()
                self.inMenu = False
        else:
            if keys[pygame.K_x] and not self.messageSent:
                self.enemySelected = None

    def run(self, dt):
        self.displaySurface.fill('Black')
        if self.cooldown > 0: self.cooldown -= 1

        # Gui
        self.displaySurface.blit(self.name, (32, 380))
        self.displaySurface.blit(self.lvLabel, (134, 380))
        self.displaySurface.blit(self.hpLabel, (296 + (self.maxHp - 20) * 1.2, 380))

        self.displaySurface.blit(self.hpTip, (226, 384))
        pygame.draw.rect(self.displaySurface, '#BF0000', (256, 380, self.maxHp * 1.2, 21))
        pygame.draw.rect(self.displaySurface, '#FFFF00', (256, 380, self.hp * 1.2, 21))

        for button in self.buttons:
            self.displaySurface.blit(button.image, button.rect)

        # Enemy
        self.enemy.update()
        self.displaySurface.blit(self.enemy.image, self.enemy.rect)

        # Spell Map Processing
        self.spellMap.update()
        self.spellMap.draw(self.displaySurface)

        # Menu & Soul Processing
        if self.menuEnabled:
            self.menuProcessing()
        else:
            self.soul.update()
            self.displaySurface.blit(self.soul.image, self.soul.rect)
            # pygame.draw.rect(self.displaySurface, 'Yellow', self.soul.hitbox)

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_f]:
            self.mapSize = (random.randint(50, 600), random.randint(50, 400))
        elif keys[pygame.K_t]:
            self.enableMenu()
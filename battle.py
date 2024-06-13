import math

from settings import *
import random

from player import Soul
from enemy import Pyhtoncheg
from functions.spell_map import SpellMap
from functions.button import Button
from functions.targetLine import TargetLine
from functions.slash import Slash
from functions.font_processor import DialogueFont, OptionFont
from functions.item import Item, Food


class Battle:
    def __init__(self):
        # Setup
        self.displaySurface = pygame.display.get_surface()
        self.menuEnabled = False
        self.mapSize = (165, 165)

        # PLayer
        self.spellMap = SpellMap(self)
        self.soul = Soul(self)
        self.soul.inventory = [Food('Pie'), Food('L. Hero')]

        # Enemy
        self.enemy = Pyhtoncheg(self)
        self.enemySelect = [OptionFont(('~Y' if self.enemy.canSpare else '') + self.enemy.name)]  # Name of one enemy by now
        self.acts = [OptionFont(option) for option in self.enemy.acts]
        self.acts.insert(0, OptionFont('Проверить'))
        self.lastHpProgress = self.enemy.hp / self.enemy.maxHp * 100
        self.attacks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.misc = pygame.sprite.Group()

        # Gui
        self.name = statusFont.render('Chara', False, 'White')
        self.lvLabel = statusFont.render('LV ' + str(self.soul.lv), False, 'White')
        self.hpLabel = statusFont.render(str(self.soul.hp) + ' / ' + str(self.soul.maxHp), False, 'White')
        self.hpTip = tipFont.render('HP', False, 'White')
        self.buttons = [Button('fight', 0), Button('act', 1), Button('item', 2), Button('mercy', 3)]
        self.targetBoard = pygame.image.load('assets/images/gui/target_board.png')
        self.targetLine = TargetLine(self)
        self.slash = Slash()

        # Navigation
        self.selected = 0  # Buttons
        self.optionSelect = 0  # Options in menus
        self.cooldown = 0  # Cooldown Before Enters
        self.inMenu = False  # Button Pressed
        self.messageSent = False  # Status message in progress
        self.battleEnded = False  # Battle Won
        self.enemySelected = None  # Selected Enemy (for Fight, Act menu)
        self.buttons[self.selected].hover(1)

        # Music
        self.theme = pygame.mixer.Sound('assets/music/Megalo_Strike_Back.ogg')
        self.theme.set_volume(.3)
        self.theme.play(loops=-1)

        # Sounds
        self.deathSound = pygame.mixer.Sound('assets/sounds/turning_into_dust.wav')
        self.menuMoveSound = pygame.mixer.Sound('assets/sounds/menu_move.wav')
        self.selectSound = pygame.mixer.Sound('assets/sounds/select.wav')
        self.damageSound = pygame.mixer.Sound('assets/sounds/damage.wav')

        self.enableMenu()

    def enableMenu(self):
        self.menuEnabled = True
        self.soul.invincibility = 0
        self.soul.image = self.soul.defImage
        self.resizeMap(575, 140)
        [self.bullets.remove(bullet) for bullet in self.bullets]
        [self.attacks.remove(attack) for attack in self.attacks]
        if self.enemy.firstStatusMessages: statusMessage = self.enemy.firstStatusMessages
        else: statusMessage = [self.enemy.name + random.choice([' приближается.', ' появился на горизонте.'])]
        self.menuDialogue = DialogueFont(*statusMessage)
        self.buttons[self.selected].hover(1)

    def enemyTurn(self):
        self.inMenu = False
        self.menuEnabled = False
        self.messageSent = False
        self.battleEnded = False
        self.enemySelected = None
        self.buttons[self.selected].hover(0)
        self.soul.hitbox.center = self.spellMap.rect.center
        self.enemySelect = [OptionFont(('~Y' if self.enemy.canSpare else '') + self.enemy.name)]
        self.enemy.turn()

    def resizeMap(self, width, height, instant = False):
        self.mapSize = (width, height)
        if instant:
            self.spellMap.width = width
            self.spellMap.height = height

    def sendMessage(self, *type):
        self.menuDialogue = DialogueFont(*type)
        self.messageSent = True

    def menuProcessing(self):
        self.getInput()
        if not self.inMenu:  # Selecting Button
            self.menuDialogue.render(self.displaySurface, (56, 254))
            self.displaySurface.blit(self.soul.image, self.buttons[self.selected].rect.topleft + pygame.Vector2(8, 13))
        elif self.messageSent:  # Status Message (after act, etc.)
            self.menuDialogue.render(self.displaySurface, (56, 254))
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_RETURN] and self.menuDialogue.done:
                if self.battleEnded: pygame.quit()
                else: self.enemyTurn()
            elif keys[pygame.K_x]:
                self.menuDialogue.done = True
                for i in range(len(self.menuDialogue.printingPos)):
                    self.menuDialogue.printingPos[i] = 100

        elif self.selected == 0:  # Fight Menu
            if self.enemySelected is None:  # Selecting Enemy
                self.enemySelection()
            else:  # Target Board (Aiming)
                self.displaySurface.blit(self.targetBoard, (47, 242))
                self.displaySurface.blit(self.targetLine.image, self.targetLine.rect)
                self.targetLine.update()
                if self.targetLine.done:  # Ending Player's Attack
                    if self.enemy.hp > 0:
                        self.enemyTurn()
                        self.slash.reset()
                        self.targetLine.reset()
                    else:
                        self.theme.stop()
                        self.deathSound.play()
                        self.battleEnded = True
                        self.enemySelected = None
                        self.sendMessage('ВЫ ПОБЕДИЛИ.', 'Вы получили 70 ОП и 15 М.')
                        [button.hover(0) for button in self.buttons]

                elif self.targetLine.pressed:  # Animation
                    self.slash.update()
                    self.displaySurface.blit(self.slash.image, self.slash.rect)

                    frame = self.targetLine.stay
                    dealtDamage = self.targetLine.dealtDamage[1]
                    if frame <= 80:
                        # Enemy's Health Bar
                        if dealtDamage > 0:
                            x, y = screenSize[0] / 2 - 50, 158
                            progressFill = self.lastHpProgress - (dealtDamage / self.enemy.maxHp * 100) * ((80 - max(frame, 40)) / 40)
                            pygame.draw.rect(self.displaySurface, 'Black', (x-1, y-1, 102, 15))
                            pygame.draw.rect(self.displaySurface, '#404040', (x, y, 100, 13))
                            pygame.draw.rect(self.displaySurface, '#0df700', (x, y, progressFill, 13))

                        # Dealt Damage Counter
                        offsetY = 0
                        if dealtDamage > 0:
                            self.enemy.offsetX = math.sin(frame / 1.2) * 20 * (frame / 120)
                            offsetY = abs(math.sin(frame / 20)) * 30 if frame > 40 else 20
                        dealtDamageLabel = self.targetLine.dealtDamage[0]
                        self.displaySurface.blit(dealtDamageLabel, (screenSize[0] / 2 - dealtDamageLabel.get_width() / 2, 100 + offsetY))

                        # Damage (Enemy Hurt) Sound
                        if frame == 80 and dealtDamage > 0:
                            self.damageSound.play()

        elif self.selected == 1:  # Act Menu
            if self.enemySelected is None:  # Selecting Enemy
                self.enemySelection()
            else:
                self.optionSelection()
                for index, option in enumerate(self.acts):
                    option.render(self.displaySurface, (96 + index % 2 * 285, 254 + index // 2 * 32))

        elif self.selected == 2:  # Item Menu
            self.optionSelection()
            for index, item in enumerate(self.soul.inventory):
                item.label.render(self.displaySurface, (96 + index % 2 * 285, 254 + index // 2 * 32))

        elif self.selected == 3:  # Mercy Menu
            self.optionSelection()
            for index, option in enumerate(self.acts):
                option.render(self.displaySurface, (96 + index % 2 * 285, 254 + index // 2 * 32))

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
        if self.selected == 1: options = self.acts  # Act Menu
        elif self.selected == 2: options = self.soul.inventory  # Item Menu
        else: options = []

        if self.optionSelect > len(options) - 1: self.optionSelect = 0
        self.displaySurface.blit(self.soul.image, pygame.Vector2(96 + self.optionSelect % 2 * 285, 254 + self.optionSelect // 2 * 32) + pygame.Vector2(-32, 4))
        lastSelected = self.optionSelect

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_RETURN] and not self.cooldown:
            if self.selected == 1:  # Act Menu
                self.enemy.act(options[self.optionSelect].value)
                self.acts = [OptionFont(option) for option in self.enemy.acts]
                self.acts.insert(0, OptionFont('Проверить'))
            elif self.selected == 2:  # Item Menu
                self.soul.inventory[self.optionSelect].use(self)
                self.soul.inventory.pop(self.optionSelect)
            self.cooldown = 5
        elif keys[pygame.K_a]:
            self.optionSelect = max(self.optionSelect - 1, 0)
        elif keys[pygame.K_d]:
            self.optionSelect = min(self.optionSelect + 1, len(options) - 1)
        elif keys[pygame.K_w]:
            self.optionSelect = max(self.optionSelect - 2, 0)
        elif keys[pygame.K_s]:
            self.optionSelect = min(self.optionSelect + 2, len(options) - 1)

        if lastSelected != self.optionSelect:
            self.menuMoveSound.play()

    def buttonHoverEffect(self, index):
        [button.hover(0) for button in self.buttons]
        self.buttons[index].hover(1)

    def getInput(self):
        keys = pygame.key.get_just_pressed()
        if not self.inMenu:
            if keys[pygame.K_RETURN] and not self.cooldown:
                if self.selected != 2 or len(self.soul.inventory):
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
        elif not (self.enemySelected or self.messageSent):
            if keys[pygame.K_x]:
                for i in range(len(self.menuDialogue.printingPos)):
                    self.menuDialogue.printingPos[i] = 0
                self.selectSound.play()
                self.inMenu = False
        else:
            if keys[pygame.K_x] and not (self.messageSent or self.selected == 0):
                self.enemySelected = None
                self.selectSound.play()

    def run(self, dt):
        self.displaySurface.fill('Black')
        if self.cooldown > 0: self.cooldown -= 1

        # Gui
        self.displaySurface.blit(self.name, (32, 380))
        self.displaySurface.blit(self.lvLabel, (134, 380))
        self.displaySurface.blit(self.hpLabel, (296 + (self.soul.maxHp - 20) * 1.2, 380))

        self.displaySurface.blit(self.hpTip, (226, 384))
        self.hpLabel = statusFont.render(str(self.soul.hp) + ' / ' + str(self.soul.maxHp), False, 'White')
        pygame.draw.rect(self.displaySurface, '#BF0000', (256, 380, self.soul.maxHp * 1.2, 21))
        pygame.draw.rect(self.displaySurface, '#FFFF00', (256, 380, self.soul.hp * 1.2, 21))

        for button in self.buttons:
            self.displaySurface.blit(button.image, button.rect)

        self.misc.update()
        self.misc.draw(self.displaySurface)

        # Enemy
        if not self.battleEnded:
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
            self.attacks.update()
            self.bullets.update()
            self.displaySurface.blit(self.soul.image, self.soul.rect)

            attacksSurf = pygame.Surface(screenSize)
            for bullet in self.bullets:
                # This to Draw Bullets' Hitboxes
                # pygame.draw.rect(self.displaySurface, 'Cyan', bullet.rect)
                attacksSurf.blit(bullet.image, bullet.rect)
                if self.soul.hitbox.colliderect(bullet.rect):
                    self.soul.hit(self.enemy.atk)
            subRect = self.spellMap.rect
            subRect.topleft += pygame.Vector2(5, 5)
            subRect.size -= pygame.Vector2(10, 10)
            attacksSurf = attacksSurf.subsurface(subRect)
            attacksSurf.set_colorkey('Black')
            self.displaySurface.blit(attacksSurf, subRect.topleft)
            # This to drawPlayer's Hitbox
            # pygame.draw.rect(self.displaySurface, 'Yellow', self.soul.hitbox)

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_f]:
            self.resizeMap(random.randint(50, 600), random.randint(50, 350))
        elif keys[pygame.K_t]:
            self.enableMenu()
        elif keys[pygame.K_m]:
            if self.theme.get_volume() > 0:
                self.theme.set_volume(0)
                print('Music Disabled')
            else:
                self.theme.set_volume(0.3)
                print('Music Enabled')
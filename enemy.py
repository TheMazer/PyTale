from settings import *

import random
from functions.import_folder import importFolder
from attacks.snakes import SnakesAttack


class Enemy(pygame.sprite.Sprite):
    def __init__(self, battleClass):
        super().__init__()
        self.soul = battleClass.soul
        self.spellMap = battleClass.spellMap
        self.sendMessage = battleClass.sendMessage

        # Setup
        self.name = 'Enemy'
        self.description = None
        self.acts = []
        self.hp = 100
        self.maxHp = 100
        self.canSpare = False
        self.canFlee = False

        self.firstStatusMessages = []
        self.statusMessages = []

    def act(self, type):
        pass


class Pyhtoncheg(Enemy):
    def __init__(self, battleClass):
        super().__init__(battleClass)
        self.hurtImage = pygame.image.load('assets/images/enemy/Pyhtoncheg/hurt.png')
        self.frames = importFolder('assets/images/enemy/Pyhtoncheg/idle')
        self.animationSpeed = 0.5
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        self.battleClass = battleClass

        self.offsetX = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.spellMap.rect.center - pygame.Vector2(self.offsetX, 155)

        # Setup
        self.name = 'Шедевропихтончег'
        self.description = 'Он по-видимому злой.'
        self.acts = ['Погладить', 'Программировать']
        self.canSpare = False
        self.canFlee = False

        self.firstStatusMessages = []
        self.statusMessages = []

        # Stats
        self.maxHp = 350
        self.hp = 350
        self.atk = 16
        self.df = 60

    def act(self, type):
        if type == 'Проверить':
            stats = f"{self.name} {self.atk} АТК {self.df} ЗАЩ"
            if self.description: self.sendMessage(stats, self.description)
            else: self.sendMessage(stats)
        elif type == 'Погладить':
            self.sendMessage('Вы пытаетесь погладит Питона. Он вас кусает.', 'Ваша СКОРОСТЬ cнижена.')
            self.soul.speed -= 1
            self.acts.remove(type)
        elif type == 'Программировать':
            self.sendMessage('Вы программируете на Python.\nУ вас ужасно получается.', 'Питон хочет прекратить битву.')
            self.acts.remove(type)
            self.canSpare = True

    def turn(self):
        attackType = random.choice(['Snakes'])
        if attackType == 'Snakes':
            SnakesAttack(self.battleClass)

    def animate(self):
        if self.offsetX != 0:
            self.image = self.hurtImage
        else:
            self.frameIndex += self.animationSpeed
            if self.frameIndex >= len(self.frames):
                self.frameIndex = 0
            self.image = self.frames[int(self.frameIndex)]

    def update(self):
        self.rect.center = self.spellMap.rect.center - pygame.Vector2(self.offsetX, 155)
        self.animate()

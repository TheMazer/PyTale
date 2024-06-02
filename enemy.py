from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, battleClass):
        super().__init__()
        self.spellMap = battleClass.spellMap
        self.sendMessage = battleClass.sendMessage

        # Setup
        self.name = 'Enemy'
        self.description = ['Enemy — 0 ATK 0 DEF']
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
        self.defImage = pygame.image.load('assets/images/enemy/Pyhtoncheg/idle/0.png')
        self.image = pygame.image.load('assets/images/enemy/Pyhtoncheg/idle/0.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.spellMap.rect.center - pygame.Vector2(0, 155)

        # Setup
        self.name = 'Шедевропихтончег'
        self.description = ['Шедевропихтончег 5 ATK 6 DEF', 'Он по-видимому злой']
        self.acts = ['Погладить', 'Программировать']
        self.hp = 350
        self.maxHp = 350
        self.canSpare = False
        self.canFlee = False

        self.firstStatusMessages = []
        self.statusMessages = []

    def act(self, type):
        if type == 'Погладить':
            self.sendMessage('Вы пытаетесь погладит Питона. Он вас кусает.', 'Ваша скорость снижена.')

    def update(self):
        self.image = pygame.transform.scale(self.defImage, (84, 138))
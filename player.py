import pygame

from settings import *
from functions.import_folder import importFolder


class Soul(pygame.sprite.Sprite):
    def __init__(self, battleClass):
        # Setup
        super().__init__()
        self.mapSize = battleClass.mapSize
        self.spellMap = battleClass.spellMap

        self.defImage = pygame.image.load('assets/images/soul/red.png')
        self.invincibilityFrames = importFolder('assets/images/soul')
        self.image = self.defImage
        self.animationSpeed = 0.1
        self.frameIndex = 0

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 8, 8)
        self.hitbox.center = self.spellMap.rect.center

        # Stats
        self.lv = 19
        self.weapon = ('Real Knife', 99)
        self.armor = ('The Locket', 99)

        self.maxHp = 4 * self.lv + 16
        self.atk = 2 * (self.lv - 1) + self.weapon[1]
        self.df = (self.lv - 1) // 4
        self.invincibilityTime = fps * 2

        self.hp = self.maxHp
        self.inventory = []

        # Controls
        self.direction = pygame.Vector2()
        self.controllability = True
        self.invincibility = 0
        self.precision = False
        self.speed = 2

        # Sounds
        self.hurtSound = pygame.mixer.Sound('assets/sounds/hurt.wav')

    def hit(self, damage):
        if not self.invincibility:
            self.invincibility = self.invincibilityTime
            self.hp = max(self.hp - max(damage - self.df, 0), 0)
            self.hurtSound.play()

    def movement(self):
        self.getInput()
        self.hitbox.topleft += self.direction * self.speed * (0.5 if self.precision else 1)
        self.rect.center = self.hitbox.center
        self.mapRestriction()

    def mapRestriction(self):
        # Horizontal Restriction
        if self.rect.left < self.spellMap.rect.left + 5:
            self.rect.left = self.spellMap.rect.left + 5
            self.hitbox.centerx = self.rect.centerx
        elif self.rect.right > self.spellMap.rect.right - 5:
            self.rect.right = self.spellMap.rect.right - 5
            self.hitbox.centerx = self.rect.centerx

        # Vertical Restriction
        if self.rect.top < self.spellMap.rect.top + 5:
            self.rect.top = self.spellMap.rect.top + 5
            self.hitbox.centery = self.rect.centery
        elif self.rect.bottom > self.spellMap.rect.bottom - 5:
            self.rect.bottom = self.spellMap.rect.bottom - 5
            self.hitbox.centery = self.rect.centery

    def animate(self):
        if self.invincibility:
            self.frameIndex += self.animationSpeed
            if self.frameIndex >= len(self.invincibilityFrames):
                self.frameIndex = 0
            self.image = self.invincibilityFrames[int(self.frameIndex)]
        else:
            self.image = self.defImage

    def getInput(self):
        self.direction.x = 0
        self.direction.y = 0

        if self.controllability:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.direction.x -= 1
            if keys[pygame.K_d]:
                self.direction.x += 1

            if keys[pygame.K_w]:
                self.direction.y -= 1
            if keys[pygame.K_s]:
                self.direction.y += 1

            self.precision = keys[pygame.K_x]

    def update(self):
        self.animate()
        self.movement()
        if self.invincibility > 0:
            self.invincibility -= 1
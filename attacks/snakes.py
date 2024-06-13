from settings import *

import random


class SnakesAttack(pygame.sprite.Sprite):
    def __init__(self, battleClass):
        super().__init__(battleClass.attacks)
        self.battleClass = battleClass
        self.frame = 0
        battleClass.resizeMap(140, 140)

    def spawnSnake(self):
        snake = Snake(self.battleClass.bullets)

        width, height = self.battleClass.mapSize
        spellMap = pygame.Rect(321 - width / 2, 300 - height / 2, width, height)
        sideNumber = random.random()

        if sideNumber < 0.25:  # Left
            snake.image = pygame.transform.rotate(snake.image, -90)
            x, y = spellMap.left + 5 - snake.image.get_width(), spellMap.top + random.randint(5, spellMap.height - 33)
            direction = pygame.Vector2(1, 0)
        elif sideNumber < 0.5:  # Right
            snake.image = pygame.transform.rotate(snake.image, 90)
            x, y = spellMap.right - 5, spellMap.top + random.randint(5, spellMap.height - 33)
            direction = pygame.Vector2(-1, 0)
        elif sideNumber < 0.75:  # Top
            snake.image = pygame.transform.flip(snake.image, False, True)
            x, y = spellMap.left + random.randint(5, spellMap.width - 33), spellMap.top - snake.image.get_height() + 5
            direction = pygame.Vector2(0, 1)
        else:  # Bottom
            x, y = spellMap.left + random.randint(5, spellMap.width - 33), spellMap.bottom - 5
            direction = pygame.Vector2(0, -1)

        snake.rect = snake.image.get_rect()
        snake.rect.topleft = x, y
        snake.direction = direction

    def update(self):
        # Spawn Snake every second
        if self.frame % fps == 0:
            self.spawnSnake()

        # End Attack after 9 seconds
        if self.frame >= fps * 9 + 20:
            self.battleClass.enableMenu()
            self.kill()
        self.frame += 1


class Snake(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('assets/images/attacks/snake.png')
        self.rect = self.image.get_rect()

        self.direction = pygame.Vector2()
        self.speed = 2

    def update(self):
        self.rect.topleft += self.direction * self.speed
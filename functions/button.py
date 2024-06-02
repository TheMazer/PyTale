from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()
        self.idleSprite = pygame.image.load('assets/images/gui/buttons/' + type + '_button.png')
        self.hoverSprite = pygame.image.load('assets/images/gui/buttons/' + type + '_button_hover.png')
        self.image = self.idleSprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos * 155 + 32 + pos // 2, 410)

    def hover(self, value):
        self.image = self.hoverSprite if value else self.idleSprite
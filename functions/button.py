from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()
        self.image = pygame.image.load('assets/images/gui/buttons/' + type + '_button.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos * 155 + 32 + pos // 2, 410)
import pygame
pygame.init()

# Screen Setup
screenSize = (640, 480)
screenFlags = 0

# Game Properties
tileSize = 64
fps = 60

# Fonts
statusFont = pygame.font.Font('assets/fonts/mars.ttf', 24)
tipFont = pygame.font.Font('assets/fonts/8bitwonder.otf', 12)
dialogueFont = pygame.font.Font('assets/fonts/determination.otf', 26)
damageFont = pygame.font.Font('assets/fonts/hachiro.ttf', 24)
damageFillFont = pygame.font.Font('assets/fonts/hachicro_inline.otf', 24)
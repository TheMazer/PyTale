from settings import *

import time
from battle import Battle


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize, flags=screenFlags)
        pygame.display.set_caption('PyTale: Undertale on Python')
        pygame.display.set_icon(pygame.image.load('assets/images/gui/icon.png'))

        self.clock = pygame.time.Clock()

        self.currentStage = None
        self.startBattle()

    def startBattle(self):
        self.currentStage = Battle()

    def run(self):
        fpsCounter = 0
        fpsUpdateInterval = 0

        running = True
        while running:
            start_time = time.time()
            dt = self.clock.tick(fps)
            self.currentStage.run(dt)
            self.screen.blit(statusFont.render(str(fpsCounter), False, 'Lime'), (16, 16))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            try: timeDiff = round(1.0 / (time.time() - start_time))
            except ZeroDivisionError: timeDiff = 0
            if fpsUpdateInterval >= 20:
                fpsCounter = timeDiff
                fpsUpdateInterval = 0
            else:
                fpsUpdateInterval += 1


if __name__ == '__main__':
    game = Game()
    game.run()
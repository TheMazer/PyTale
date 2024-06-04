from settings import *

from functions.font_processor import OptionFont


itemsTypes = {
    'Pie': {
        'name': 'Пирог',
        'heal': 99
    },
    'L. Hero': {
        'name': 'Л.Герой',
        'ate': 'Легендарного героя',
        'heal': 40
    }
}


class Item:
    def __init__(self, type):
        self.name = itemsTypes[type]['name']
        self.label = OptionFont(self.name)

    def use(self, battleClass):
        pass


class Food(Item):
    def __init__(self, type):
        super().__init__(type)
        self.type = type
        self.heal = itemsTypes[type]['heal']
        self.displayName = itemsTypes[type].get('ate')
        self.healSound = pygame.mixer.Sound('assets/sounds/heal.wav')

    def use(self, battleClass):
        currentHp = battleClass.soul.hp
        displayName = self.name if self.displayName is None else self.displayName
        if currentHp + self.heal >= battleClass.soul.maxHp:
            battleClass.soul.hp = battleClass.soul.maxHp
            recoverMessage = 'Ваши ОЗ были полностью восстановлены.'
        else:
            battleClass.soul.hp += self.heal
            recoverMessage = 'Вы восстановили ' + str(self.heal) + ' ОЗ!'

        battleClass.sendMessage('Вы съели ' + displayName + '.', recoverMessage)
        self.healSound.play()
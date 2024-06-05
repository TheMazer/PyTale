from settings import *

from textwrap import wrap


class DialogueFont:
    def __init__(self, *text):
        self.lines = []
        self.done = False
        self.charOffset = 16
        self.printingPos = []
        self.printingSpeed = 3
        self.printingSound = pygame.mixer.Sound('assets/sounds/generic_speech.wav')
        self.printingSound.set_volume(.5)
        self.commandSymbol = False
        self.color = 'White'

        # Dotting
        formattedText = ""
        for paragraph in text:
            if paragraph.startswith("~"):
                formattedText += f"{paragraph[:2]}* {paragraph[2:]}\n"
            else:
                formattedText += f"* {paragraph}\n"

        # Wrapping Text
        lines = []
        text = formattedText.split('\n')
        for line in text:
            par = wrap(line, width=33)
            lines.extend(par)

        for line in lines:
            if not (line.startswith('* ') or line.startswith('~')):
                line = '  ' + line
            self.lines.append([])

            # Rendering Surfaces
            for char in line:
                if self.commandSymbol:
                    self.commandSymbol = False
                    if char == 'Y':
                        self.color = 'Yellow'
                else:
                    if char == "\n": self.lines.append([])
                    elif char == "~": self.commandSymbol = True
                    else: self.lines[-1].append([dialogueFont.render(char, False, self.color), char])
                    self.printingPos.append(0)

    def render(self, surf: pygame.Surface, pos):
        offsetY = 0

        for index, line in enumerate(self.lines):
            self.printingPos[index] += 1
            printingPos = self.printingPos[index]
            offsetX = 0

            printableSymbols = line[:printingPos // self.printingSpeed]
            notSilentSymbol = printableSymbols and printableSymbols[-1][1] not in (' ', '.', ',')
            newSymbol = printingPos % self.printingSpeed == 0
            notEnd = printingPos // self.printingSpeed <= len(line)

            if notSilentSymbol and newSymbol and notEnd:
                self.printingSound.play(maxtime=fps*self.printingSpeed)
            for char in printableSymbols:
                snip = char[0]
                surf.blit(snip, (pos[0] + offsetX, pos[1] + offsetY))
                offsetX += max(snip.get_width() + 2, self.charOffset) if char[1] != '*' else self.charOffset
            offsetY += 32

            self.done = False
            if notEnd: break
            self.done = True

            # Todo: For multiple messages create callback


class OptionFont(DialogueFont):
    def __init__(self, *text):
        super().__init__(*text)
        self.value = text[0]

    def render(self, surf: pygame.Surface, pos):
        offsetY = 0

        for line in self.lines:
            offsetX = 0

            for char in line:
                snip = char[0]
                surf.blit(snip, (pos[0] + offsetX, pos[1] + offsetY))
                offsetX += max(snip.get_width() + 2, self.charOffset)
            offsetY += 32
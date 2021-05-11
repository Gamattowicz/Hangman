import os
import random
from pathlib import Path


class Game:
    def __init__(self, width, height, radius, gap):
        self.width = width
        self.height = height
        self.radius = radius
        self.gap = gap
        self.letters = []
        self.words = []
        self.word = ''
        self.guessed = []

    def draw_letters(self):
        # First row coordinates
        startx = round((self.width - (self.radius * 2 + self.gap) * 10) / 2)
        starty = 475
        qwerty_keyboard = 'QWERTYUIOP'
        for i in range(10):
            x = startx + self.gap * 2 + (self.radius * 2 + self.gap) * (i % 10)
            y = starty + ((i // 10) * (self.gap + self.radius * 2))
            self.letters.append([x, y, qwerty_keyboard[i], True, False])

        # Second row coordinates
        startx2 = round((self.width - (self.radius * 2 + self.gap) * 9) / 2)
        starty2 = starty + (self.radius * 2 + self.gap)
        qwerty_keyboard2 = 'ASDFGHJKL'
        for i in range(9):
            x = startx2 + self.gap * 2 + (self.radius * 2 + self.gap) * (i % 9)
            y = starty2 + ((i // 9) * (self.gap + self.radius * 2))
            self.letters.append([x, y, qwerty_keyboard2[i], True, False])

        # Third row coordinates
        startx3 = round((self.width - (self.radius * 2 + self.gap) * 7) / 2)
        starty3 = starty + 2 * (self.radius * 2 + self.gap)
        qwerty_keyboard3 = 'ZXCVBNM'
        for i in range(7):
            x = startx3 + self.gap * 2 + (self.radius * 2 + self.gap) * (i % 7)
            y = starty3 + ((i // 7) * (self.gap + self.radius * 2))
            self.letters.append([x, y, qwerty_keyboard3[i], True, False])

        filename = 'words.csv'
        base_dir = Path(__file__).resolve().parent
        path = os.path.join(base_dir, filename)
        with open(path, 'r') as f:
            for line in f:
                self.words.append(line[:-1])
        self.word = random.choice(self.words).upper()
        print(self.word)
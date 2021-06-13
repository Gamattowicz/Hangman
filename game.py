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

    def draw_letters(self, player):
        # First row coordinates
        start_x = round((self.width - (self.radius * 2 + self.gap) * 10) / 2)
        start_y = 475
        qwerty_keyboard = 'QWERTYUIOP'
        for i in range(10):
            x = start_x + self.gap * 2 + (self.radius * 2 + self.gap) * (i % 10)
            y = start_y + ((i // 10) * (self.gap + self.radius * 2))
            self.letters.append([x, y, qwerty_keyboard[i], True, False])

        # Second row coordinates
        start_x2 = round((self.width - (self.radius * 2 + self.gap) * 9) / 2)
        start_y2 = start_y + (self.radius * 2 + self.gap)
        qwerty_keyboard2 = 'ASDFGHJKL'
        for i in range(9):
            x = start_x2 + self.gap * 2 + (self.radius * 2 + self.gap) * (i % 9)
            y = start_y2 + ((i // 9) * (self.gap + self.radius * 2))
            self.letters.append([x, y, qwerty_keyboard2[i], True, False])

        # Third row coordinates
        start_x3 = round((self.width - (self.radius * 2 + self.gap) * 7) / 2)
        start_y3 = start_y + 2 * (self.radius * 2 + self.gap)
        qwerty_keyboard3 = 'ZXCVBNM'
        for i in range(7):
            x = start_x3 + self.gap * 2 + (self.radius * 2 + self.gap) * (i % 7)
            y = start_y3 + ((i // 7) * (self.gap + self.radius * 2))
            self.letters.append([x, y, qwerty_keyboard3[i], True, False])

        filename = 'words.csv'
        base_dir = Path(__file__).resolve().parent
        path = os.path.join(base_dir, filename)
        with open(path, 'r') as f:
            for line in f:
                self.words.append(line[:-1])
        for i in range(100):
            word = random.choice(self.words).upper()
            if player.difficulty == 1:
                if len(word) < 5:
                    self.word = word
                    break
            elif player.difficulty == 2:
                if 5 < len(word) < 8:
                    self.word = word
                    break
            else:
                if len(word) > 8:
                    self.word = word
                    break
        print(self.word)
import pygame
import os
from math import sqrt

# Display variables
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HANGMAN GAME')
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
LETTER_FONT = pygame.font.SysFont('arial', 40)
WORD_FONT = pygame.font.SysFont('arial', 60)

# Button variables
RADIUS = 30
GAP = 20
letters = []

# First row coordinates
startx = round((WIDTH - (RADIUS * 2 + GAP) * 10) / 2)
starty = 375
qwerty_keyboard = 'qwertyuiop'
for i in range(10):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 10)
    y = starty + ((i // 10) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard[i], True])

# Second row coordinates
startx2 = round((WIDTH - (RADIUS * 2 + GAP) * 9) / 2)
starty2 = starty + (RADIUS * 2 + GAP)
qwerty_keyboard2 = 'asdfghjkl'
for i in range(9):
    x = startx2 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 9)
    y = starty2 + ((i // 9) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard2[i], True])

# Third row coordinates
startx3 = round((WIDTH - (RADIUS * 2 + GAP) * 7) / 2)
starty3 = starty + 2 * (RADIUS * 2 + GAP)
qwerty_keyboard3 = 'zxcvbnm'
for i in range(7):
    x = startx3 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 7)
    y = starty3 + ((i // 7) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard3[i], True])

# Load assets
HANGMAN_IMAGES = [pygame.image.load(os.path.join('Assets', f'hangman'
                                                 f'{num}.png')) for num in range(7)]

# Game variables
FPS = 60
mistakes = 0
word = 'developer'
guessed = []


def draw():
    WIN.fill(WHITE)

    # draw word
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ''
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, 1, BLACK)
    WIN.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(WIN, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    WIN.blit(HANGMAN_IMAGES[mistakes], (150, 50))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dist = sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                        if dist < RADIUS:
                            letter[3] = False
    pygame.quit()


if __name__ == '__main__':
    main()
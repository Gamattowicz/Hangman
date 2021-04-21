import pygame
import os
from math import sqrt
import random

# Display variables
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HANGMAN GAME')
pygame.init()
timer = 0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
LETTER_FONT = pygame.font.SysFont('arial', 40)
WORD_FONT = pygame.font.SysFont('arial', 60)
TITLE_FONT = pygame.font.SysFont('arial', 70)

# Button variables
RADIUS = 30
GAP = 20
letters = []

# First row coordinates
startx = round((WIDTH - (RADIUS * 2 + GAP) * 10) / 2)
starty = 375
qwerty_keyboard = 'QWERTYUIOP'
for i in range(10):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 10)
    y = starty + ((i // 10) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard[i], True])

# Second row coordinates
startx2 = round((WIDTH - (RADIUS * 2 + GAP) * 9) / 2)
starty2 = starty + (RADIUS * 2 + GAP)
qwerty_keyboard2 = 'ASDFGHJKL'
for i in range(9):
    x = startx2 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 9)
    y = starty2 + ((i // 9) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard2[i], True])

# Third row coordinates
startx3 = round((WIDTH - (RADIUS * 2 + GAP) * 7) / 2)
starty3 = starty + 2 * (RADIUS * 2 + GAP)
qwerty_keyboard3 = 'ZXCVBNM'
for i in range(7):
    x = startx3 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 7)
    y = starty3 + ((i // 7) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard3[i], True])

# Load assets
HANGMAN_IMAGES = [pygame.image.load(os.path.join('Assets', f'hangman'
                                                 f'{num}.png')) for num in range(7)]

# Game variables
mistakes_number = 0
words = ['FIRST', 'SECOND', 'THIRD', 'DEVELOPER']
word = random.choice(words)
guessed = []


def draw():
    WIN.fill(WHITE)

    # draw title
    text = TITLE_FONT.render('HANGMAN GAME', 1, BLACK)
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, 1, BLACK)
    WIN.blit(text, (350, 175))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(WIN, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # draw image
    WIN.blit(HANGMAN_IMAGES[mistakes_number], (100, 100))

    # draw timer
    mins = timer // 60
    formatted_mins = f'0{mins}' if mins < 10 else mins
    secs = timer - mins * 60
    formatted_secs = f'0{secs}' if secs < 10 else secs
    watch = TITLE_FONT.render(f'Timer {formatted_mins}:{formatted_secs}', 1, BLACK)
    WIN.blit(watch, (550, 100))
    pygame.display.update()


def display_result(msg):
    pygame.time.delay(1500)
    WIN.fill(WHITE)
    text = WORD_FONT.render(msg, 1, BLACK)
    WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 -
                    text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    global mistakes_number
    global timer

    time_elapsed = 0
    clock = pygame.time.Clock()
    run = True
    while run:
        time_elapsed += clock.get_rawtime()
        clock.tick()

        if time_elapsed / 1000 > 1:
            time_elapsed = 0
            timer += 1

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
                            pygame.time.delay(200)
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                mistakes_number += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_result('You Won!')
            break

        if mistakes_number == 6:
            display_result('You Lost!')
            break

    pygame.quit()


if __name__ == '__main__':
    main()
import pygame
import os
from math import sqrt
import random
import sys
from pathlib import Path
from player import Player
from menu import draw_menu, pause, BACKGROUND_COLOR
from leaderboard import get_leaderboard

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
    letters.append([x, y, qwerty_keyboard[i], True, False])

# Second row coordinates
startx2 = round((WIDTH - (RADIUS * 2 + GAP) * 9) / 2)
starty2 = starty + (RADIUS * 2 + GAP)
qwerty_keyboard2 = 'ASDFGHJKL'
for i in range(9):
    x = startx2 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 9)
    y = starty2 + ((i // 9) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard2[i], True, False])

# Third row coordinates
startx3 = round((WIDTH - (RADIUS * 2 + GAP) * 7) / 2)
starty3 = starty + 2 * (RADIUS * 2 + GAP)
qwerty_keyboard3 = 'ZXCVBNM'
for i in range(7):
    x = startx3 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 7)
    y = starty3 + ((i // 7) * (GAP + RADIUS * 2))
    letters.append([x, y, qwerty_keyboard3[i], True, False])

# Load assets
HANGMAN_IMAGES = [pygame.image.load(os.path.join('Assets', f'hangman'
                                                 f'{num}.png')) for num in range(7)]

# Game variables
words = []
filename = 'words.csv'
base_dir = Path(__file__).resolve().parent
path = os.path.join(base_dir, filename)
with open(path, 'r') as f:
    for line in f:
        words.append(line[:-1])
word = random.choice(words).upper()
print(word)
guessed = []


def draw(player):
    WIN.fill(WHITE)

    # draw title
    text = TITLE_FONT.render('HANGMAN GAME', True, BLACK)
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, True, BLACK)
    WIN.blit(text, (350, 175))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible, clicked = letter
        if visible:
            if clicked:
                pygame.draw.circle(WIN, (255, 0, 0), (x, y), RADIUS, 3)
            else:
                pygame.draw.circle(WIN, BLACK, (x, y), RADIUS, 3)

            text = LETTER_FONT.render(ltr, True, BLACK)
            WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # draw image
    WIN.blit(HANGMAN_IMAGES[player.lives], (100, 100))

    # draw timer
    watch = TITLE_FONT.render(f'Timer {player.format_timer()}', True, BLACK)
    WIN.blit(watch, (550, 100))

    # draw lives
    lives = TITLE_FONT.render(f'Lives: {player.lives}', True, BLACK)
    WIN.blit(lives, (550, 250))
    pygame.display.update()


def display_result(msg):
    pygame.time.delay(1500)
    WIN.fill(WHITE)
    text = WORD_FONT.render(msg, True, BLACK)
    WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 -
                    text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main(player):
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
            player.timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(WIN, WIDTH, HEIGHT, main, main_menu, get_leaderboard, player)
                elif event.unicode.isalpha():
                    for letter in letters:
                        x, y, ltr, visible, clicked = letter
                        if ltr == event.unicode.upper():
                            letter[4] = True
                            draw(player)
                            pygame.time.delay(200)
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                player.lives -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible, clicked = letter
                    if visible:
                        dist = sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                        if dist < RADIUS:
                            letter[4] = True
                            draw(player)
                            pygame.time.delay(200)
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                player.lives -= 1

        draw(player)

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            player.score += 10
            player.save_score(player.format_timer)
            display_result('You Won!')
            break

        if player.lives == 0:
            display_result('You Lost!')
            break

    pygame.quit()
    sys.exit()


def main_menu(surface):
    active = 1
    player = Player()
    run = True

    while run:
        surface.fill(BACKGROUND_COLOR)
        buttons = ['NEW GAME', 'LEADERBOARD', 'EXIT']
        draw_menu(surface, 'MAIN MENU', buttons, WIDTH, HEIGHT, active)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if active == 3:
                        active = 1
                    else:
                        active += 1
                elif event.key == pygame.K_UP:
                    if active == 1:
                        active = 3
                    else:
                        active -= 1
                elif event.key == pygame.K_RETURN:
                    if active == 1:
                        main(player)
                    elif active == 2:
                        get_leaderboard(surface, WIDTH, HEIGHT)
                    elif active == 3:
                        pygame.quit()
                        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu(WIN)
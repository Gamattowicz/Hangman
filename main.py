import pygame
from math import sqrt
import sys
from player import Player
from menu import draw_menu, pause, BACKGROUND_COLOR
from leaderboard import get_leaderboard
from board import Board
from game import Game

# Display variables
WIDTH, HEIGHT = 1200, 700
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


def draw(player, game, board):
    WIN.fill(BACKGROUND_COLOR)

    # draw title
    text = TITLE_FONT.render('HANGMAN GAME', True, BLACK)
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ''
    for letter in game.word:
        if letter in game.guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, True, BLACK)
    WIN.blit(text, (350, 175))

    # draw buttons
    for letter in game.letters:
        x, y, ltr, visible, clicked = letter
        if visible:
            if clicked:
                pygame.draw.circle(WIN, (255, 0, 0), (x, y), game.radius, 3)
            else:
                pygame.draw.circle(WIN, BLACK, (x, y), game.radius, 3)

            text = LETTER_FONT.render(ltr, True, BLACK)
            WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # draw image
    WIN.blit(board.HANGMAN_IMAGES[player.lives], (100, 100))

    # draw timer
    watch = TITLE_FONT.render(f'Timer {player.format_timer()}', True, BLACK)
    WIN.blit(watch, (850, 100))

    # draw lives
    lives = TITLE_FONT.render(f'Lives: {player.lives}', True, BLACK)
    WIN.blit(lives, (850, 250))
    pygame.display.update()


def main(player, surface):
    global timer
    time_elapsed = 0
    board = Board(WIDTH, HEIGHT)
    game = Game(WIDTH, HEIGHT, 30, 20)
    game.draw_letters()
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
                    for letter in game.letters:
                        x, y, ltr, visible, clicked = letter
                        if ltr == event.unicode.upper():
                            letter[4] = True
                            draw(player, game, board)
                            pygame.time.delay(200)
                            letter[3] = False
                            game.guessed.append(ltr)
                            if ltr not in game.word:
                                player.lives -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in game.letters:
                    x, y, ltr, visible, clicked = letter
                    if visible:
                        dist = sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                        if dist < game.radius:
                            letter[4] = True
                            draw(player, game, board)
                            pygame.time.delay(200)
                            letter[3] = False
                            game.guessed.append(ltr)
                            if ltr not in game.word:
                                player.lives -= 1

        draw(player, game, board)

        won = True
        for letter in game.word:
            if letter not in game.guessed:
                won = False
                break

        if won:
            player.score += 10
            player.save_score(player.format_timer)
            board.draw_name(surface, player, board, main, game.word)
            break

        if player.lives == 0:
            board.draw_name(surface, player, board, main, game.word)
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
                        main(player, surface)
                    elif active == 2:
                        get_leaderboard(surface, WIDTH, HEIGHT)
                    elif active == 3:
                        pygame.quit()
                        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu(WIN)
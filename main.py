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


def main(player, surface):
    time_elapsed = 0
    board = Board(WIDTH, HEIGHT)
    game = Game(WIDTH, HEIGHT, 30, 20)
    game.draw_letters(player)
    clock = pygame.time.Clock()
    run = True
    while run:
        time_elapsed += clock.get_rawtime()
        clock.tick()

        if time_elapsed / 1000 > 1:
            time_elapsed = 0
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
                            board.draw(surface, player, game, board)
                            pygame.time.delay(200)
                            letter[3] = False
                            game.guessed.append(ltr)
                            if ltr not in game.word:
                                player.lives -= 1
                                if player.lives == 0:
                                    board.draw(surface, player, game, board)
                                    pygame.time.delay(1000)
                                    board.draw_name(surface, player, board, main, game.word, 'Lost')
                                    break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in game.letters:
                    x, y, ltr, visible, clicked = letter
                    if visible:
                        dist = sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)
                        if dist < game.radius:
                            letter[4] = True
                            board.draw(surface, player, game, board)
                            pygame.time.delay(500)
                            letter[3] = False
                            game.guessed.append(ltr)
                            if ltr not in game.word:
                                player.lives -= 1
                                if player.lives == 0:

                                    board.draw(surface, player, game, board)
                                    pygame.time.delay(500)
                                    board.draw_name(surface, player, board, main, game.word, 'Lost')
                                    break

        board.draw(surface, player, game, board)

        won = True
        for letter in game.word:
            if letter not in game.guessed:
                won = False
                break

        if won:
            player.score += 10 * len(game.word)
            board.draw(surface, player, game, board)
            pygame.time.delay(500)
            board.draw_name(surface, player, board, main, game.word, 'Won')
            break



    pygame.quit()
    sys.exit()


def main_menu(surface):
    active = 1
    player = Player()
    run = True
    difficulties = ['LOW', 'MEDIUM', 'HARD']

    while run:
        surface.fill(BACKGROUND_COLOR)
        buttons = ['NEW GAME', f'LEVEL OF DIFFICULTY: {difficulties[player.difficulty - 1]}', 'LEADERBOARD', 'EXIT']
        draw_menu(surface, 'MAIN MENU', buttons, WIDTH, HEIGHT, active)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if active == 4:
                        active = 1
                    else:
                        active += 1
                elif event.key == pygame.K_UP:
                    if active == 1:
                        active = 4
                    else:
                        active -= 1
                elif event.key == pygame.K_RETURN:
                    if active == 1:
                        main(player, surface)
                    elif active == 2:
                        if player.difficulty == 3:
                            player.difficulty = 1
                        else:
                            player.difficulty += 1
                    elif active == 3:
                        get_leaderboard(surface, WIDTH, HEIGHT)
                    elif active == 4:
                        pygame.quit()
                        sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu(WIN)
import pygame
import sys
import os
from menu import ACTIVE_COLOR, BACKGROUND_COLOR, TEXT_COLOR, SIDE_FONT, TITLE_FONT

BUTTON_FONT = pygame.font.Font('Cairo-SemiBold.ttf', 30)
PASSWORD_FONT = pygame.font.Font('Cairo-SemiBold.ttf', 50)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.active = 1

        # Load assets
        self.HANGMAN_IMAGES = [pygame.image.load(os.path.join('Assets', f'hangman'
                                                 f'{num}.png')) for num in range(7)]

    def draw_name(self, surface, player, board, main, word, win):
        draw = True
        while draw:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        player.name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        player.name = player.name[:-1]
                    elif event.key == pygame.K_RETURN or event.type == pygame.QUIT:
                        draw = False
            surface.fill(BACKGROUND_COLOR)

            lost_text = SIDE_FONT.render(f'You {win}! Password was {word}', True, TEXT_COLOR)
            surface.blit(lost_text, (self.width / 2 - lost_text.get_width() / 2, self.height / 10))

            input_text = SIDE_FONT.render('Enter your name:', True, TEXT_COLOR)
            surface.blit(input_text, (self.width / 2 - input_text.get_width() / 2, self.height / 4 + 50))

            block = SIDE_FONT.render(player.name, True, TEXT_COLOR)
            rect = block.get_rect()
            rect.center = surface.get_rect().center
            surface.blit(block, rect)
            pygame.display.update()

        if player.score > 0:
            player.save_score(player.format_timer)
        board.draw_lost_text(surface, player, main)

    def draw_lost_text(self, surface, player, main):
        lost = True

        while lost:
            surface.fill(BACKGROUND_COLOR)

            retry_text = SIDE_FONT.render('Do you want to play again?', True, TEXT_COLOR)
            surface.blit(retry_text, (self.width / 2 - retry_text.get_width() / 2, self.height / 5))

            retry_options = [('YES', 150), ('NO', - 150)]
            for i, v in enumerate(retry_options, start=1):
                if i == self.active:
                    label = SIDE_FONT.render(v[0], True, ACTIVE_COLOR)
                else:
                    label = SIDE_FONT.render(v[0], True, TEXT_COLOR)
                surface.blit(label, (self.width / 2 - label.get_width() / 2 - v[1], self.height / 3 + 100))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.active == 2:
                            self.active = 1
                        else:
                            self.active += 1
                    elif event.key == pygame.K_LEFT:
                        if self.active == 1:
                            self.active = 2
                        else:
                            self.active -= 1
                    elif event.key == pygame.K_RETURN:
                        if self.active == 1:
                            player.restart_stats()
                            main(player, surface)
                        elif self.active == 2:
                            pygame.quit()
                            sys.exit()

    def draw(self, surface, player, game, board):
        surface.fill(BACKGROUND_COLOR)

        # draw title
        text = TITLE_FONT.render('HANGMAN GAME', True, TEXT_COLOR)
        surface.blit(text, (self.width / 2 - text.get_width() / 2, 20))

        # draw word
        display_word = ''
        for letter in game.word:
            if letter in game.guessed:
                display_word += letter + ' '
            else:
                display_word += '_ '
        text = PASSWORD_FONT.render(display_word, True, TEXT_COLOR)
        surface.blit(text, (350, 175))

        # draw buttons
        for letter in game.letters:
            x, y, ltr, visible, clicked = letter
            if visible:
                if clicked:
                    pygame.draw.circle(surface, ACTIVE_COLOR, (x, y), game.radius, 3)
                    text = BUTTON_FONT.render(ltr, True, ACTIVE_COLOR)
                else:
                    pygame.draw.circle(surface, TEXT_COLOR, (x, y), game.radius, 3)
                    text = BUTTON_FONT.render(ltr, True, TEXT_COLOR)
                surface.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        # draw image
        surface.blit(board.HANGMAN_IMAGES[player.lives], (100, 100))

        # draw timer
        watch = TITLE_FONT.render(f'Timer {player.format_timer()}', True, TEXT_COLOR)
        surface.blit(watch, (850, 100))

        # draw lives
        lives = TITLE_FONT.render(f'Lives: {player.lives}', True, TEXT_COLOR)
        surface.blit(lives, (850, 250))
        pygame.display.update()
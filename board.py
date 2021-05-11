import pygame
import sys
from menu import ACTIVE_COLOR, BACKGROUND_COLOR, TEXT_COLOR, SIDE_FONT


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.active = 1

    def draw_name(self, surface, player, board, main, word):
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

            lost_text = SIDE_FONT.render(f'You Lost! Password was {word}', True, TEXT_COLOR)
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
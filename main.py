import pygame
import os

# Display variables
WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HANGMAN GAME')

# Colors
WHITE = (255, 255, 255)

# Load assets
HANGMAN_IMAGES = [pygame.image.load(os.path.join('Assets', f'hangman'
                                                 f'{num}.png')) for num in range(7)]

# Game variables
FPS = 60
mistakes = 0


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        WIN.fill(WHITE)
        WIN.blit(HANGMAN_IMAGES[mistakes], (150, 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
    pygame.quit()


if __name__ == '__main__':
    main()
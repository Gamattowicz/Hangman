import pygame
import os

# Display variables
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('HANGMAN GAME')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button variables
RADIUS = 30
GAP = 20
letters = []

# First row coordinates
startx = round((WIDTH - (RADIUS * 2 + GAP) * 10) / 2)
starty = 375
for i in range(10):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 10)
    y = starty + ((i // 10) * (GAP + RADIUS * 2))
    letters.append([x, y])

# Second row coordinates
startx2 = round((WIDTH - (RADIUS * 2 + GAP) * 9) / 2)
starty2 = starty + (RADIUS * 2 + GAP)
for i in range(9):
    x = startx2 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 9)
    y = starty2 + ((i // 9) * (GAP + RADIUS * 2))
    letters.append([x, y])

# Third row coordinates
startx3 = round((WIDTH - (RADIUS * 2 + GAP) * 7) / 2)
starty3 = starty + 2 * (RADIUS * 2 + GAP)
for i in range(7):
    x = startx3 + GAP * 2 + (RADIUS * 2 + GAP) * (i % 7)
    y = starty3 + ((i // 7) * (GAP + RADIUS * 2))
    letters.append([x, y])

# Load assets
HANGMAN_IMAGES = [pygame.image.load(os.path.join('Assets', f'hangman'
                                                 f'{num}.png')) for num in range(7)]

# Game variables
FPS = 60
mistakes = 0


def draw():
    WIN.fill(WHITE)

    # draw buttons
    for letter in letters:
        x, y = letter
        pygame.draw.circle(WIN, BLACK, (x, y), RADIUS, 3)

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
                print(pygame.mouse.get_pos())
    pygame.quit()


if __name__ == '__main__':
    main()
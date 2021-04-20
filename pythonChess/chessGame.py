import pygame
from pieceData import pieceImages
import chess

pygame.init()

board = chess.Board()
# Set up the drawing window
screen = pygame.display.set_mode([1920, 1000])
# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for rank in range(8):
        for file in range(8):
            currentSquare = pygame.Rect(580+rank*95, 160+file*95, 95, 95)
            if (file + rank) % 2:
                pygame.draw.rect(screen, (181, 136, 99), currentSquare)
            else:
                pygame.draw.rect(screen, (240, 217, 181), currentSquare)

    pygame.display.flip()

pygame.quit()

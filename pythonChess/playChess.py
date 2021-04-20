import pygame
from pieceData import pieceImages

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

TILESIZE = 95
BOARD_POS = (580, 160)


def create_board_surf():
    board_surf = pygame.Surface((TILESIZE * 8, TILESIZE * 8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color((181, 136, 99) if dark else (240, 217, 181)), rect)
            dark = not dark
        dark = not dark
    return board_surf


def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0:
            return board[y][x], x, y
    except IndexError:
        pass
    return None, None, None


def create_board():
    board = []
    for y in range(8):
        board.append([])
        for x in range(8):
            board[y].append(None)
    return board


def draw_pieces(screen, board, selected_piece):
    sx, sy = None, None
    if selected_piece:
        piece, sx, sy = selected_piece

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece:
                selected = x == sx and y == sy
                image = pygame.image.load(pieceImages[piece])
                screen.blit(image, (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE))
                pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE + 1, BOARD_POS[1] + y * TILESIZE + 1, TILESIZE, TILESIZE)


def draw_selector(screen, piece, x, y):
    if piece is not None:
        rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)


def draw_drag(screen, board, selected_piece):
    if selected_piece:
        piece, x, y = get_square_under_mouse(board)
        if x is not None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        pos = pygame.Vector2(pygame.mouse.get_pos())
        image = pygame.image.load(pieceImages[selected_piece[0]])
        screen.blit(image, image.get_rect(center=pos))
        return x, y


def loadFromFEN(FEN, board):
    rank = 0
    file = 0
    for i in FEN:
        try:
            file += int(i) - 1
        except ValueError:
            if i == "/":
                file = -1
                rank += 1
            else:
                board[rank][file] = i
        file += 1


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1000))
    board = create_board()
    loadFromFEN(startingFen, board)
    board_surf = create_board_surf()
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    while True:
        events = pygame.event.get()
        piece, x, y = get_square_under_mouse(board)
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if piece is not None:
                    selected_piece = piece, x, y
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    piece, old_x, old_y = selected_piece
                    board[old_y][old_x] = None
                    new_x, new_y = drop_pos
                    board[new_y][new_x] = piece
                selected_piece = None
                drop_pos = None

        screen.fill(pygame.Color('black'))
        screen.blit(board_surf, BOARD_POS)
        draw_pieces(screen, board, selected_piece)
        draw_selector(screen, piece, x, y)
        drop_pos = draw_drag(screen, board, selected_piece)

        if x is not None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()

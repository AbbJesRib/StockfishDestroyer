import pygame
from pieceData import pieceImages

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/1PPPPPPP/RNBQKBNR"

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


def generateLegalMovesForColor(board, isWhite):
    legalMoves = []
    for rank in range(8):
        for file in range(8):
            if type(board[rank][file]) is str:
                if board[rank][file].isupper() == isWhite:
                    if board[rank][file].upper() == 'R':
                        bannedDirections = []
                        for i in range(1, 8):
                            directions = [(rank + i, file), (rank - i, file), (rank, file + i), (rank, file - i)]
                            for y, x in directions:
                                if 0 <= x <= 7 and 0 <= y <= 7:
                                    if board[y][x] is None:
                                        pass
                                    else:
                                        if board[rank][file].isupper() != board[y][x].isupper() and directions.index(
                                                (y, x)) not in bannedDirections:
                                            legalMoves.append((y, x))
                                        bannedDirections.append(directions.index((y, x)))
                                else:
                                    bannedDirections.append(directions.index((y, x)))

                            directions = [i for i in directions if directions.index(i) not in bannedDirections]
                            legalMoves += directions
                    elif board[rank][file].upper() == 'B':
                        bannedDirections = []
                        for i in range(1, 8):
                            directions = [(rank + i, file + i), (rank - i, file + i), (rank + i, file - i),
                                          (rank - i, file - i)]
                            for y, x in directions:
                                if 0 <= x <= 7 and 0 <= y <= 7:
                                    if board[y][x] is None:
                                        pass
                                    else:
                                        if board[rank][file].isupper() != board[y][x].isupper() and directions.index(
                                                (y, x)) not in bannedDirections:
                                            legalMoves.append((y, x))
                                        bannedDirections.append(directions.index((y, x)))
                                else:
                                    bannedDirections.append(directions.index((y, x)))

                            directions = [i for i in directions if directions.index(i) not in bannedDirections]
                            legalMoves += directions
                    elif board[rank][file].upper() == 'Q':
                        bannedDirections = []
                        for i in range(1, 8):
                            directions = [(rank + i, file + i), (rank - i, file + i), (rank + i, file - i),
                                          (rank - i, file - i), (rank + i, file), (rank - i, file), (rank, file + i),
                                          (rank, file - i)]
                            for y, x in directions:
                                if 0 <= x <= 7 and 0 <= y <= 7:
                                    if board[y][x] is None:
                                        pass
                                    else:
                                        if board[rank][file].isupper() != board[y][x].isupper() and directions.index(
                                                (y, x)) not in bannedDirections:
                                            legalMoves.append((y, x))
                                        bannedDirections.append(directions.index((y, x)))
                                else:
                                    bannedDirections.append(directions.index((y, x)))

                            directions = [i for i in directions if directions.index(i) not in bannedDirections]
                            legalMoves += directions
    return legalMoves


def generateLegalMovesForPiece(board, rank, file):
    legalMoves = []
    if type(board[rank][file]) is str:
        if board[rank][file].upper() == 'R':
            bannedDirections = []
            for i in range(1, 8):
                directions = [(rank + i, file), (rank - i, file), (rank, file + i), (rank, file - i)]
                for y, x in directions:
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        if board[y][x] is None:
                            pass
                        else:
                            if board[rank][file].isupper() != board[y][x].isupper() and directions.index(
                                    (y, x)) not in bannedDirections:
                                legalMoves.append((y, x))
                            bannedDirections.append(directions.index((y, x)))
                    else:
                        bannedDirections.append(directions.index((y, x)))

                directions = [i for i in directions if directions.index(i) not in bannedDirections]
                legalMoves += directions
        elif board[rank][file].upper() == 'B':
            bannedDirections = []
            for i in range(1, 8):
                directions = [(rank + i, file + i), (rank - i, file + i), (rank + i, file - i),
                              (rank - i, file - i)]
                for y, x in directions:
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        if board[y][x] is None:
                            pass
                        else:
                            if board[rank][file].isupper() != board[y][x].isupper() and directions.index(
                                    (y, x)) not in bannedDirections:
                                legalMoves.append((y, x))
                            bannedDirections.append(directions.index((y, x)))
                    else:
                        bannedDirections.append(directions.index((y, x)))

                directions = [i for i in directions if directions.index(i) not in bannedDirections]
                legalMoves += directions
        elif board[rank][file].upper() == 'Q':
            bannedDirections = []
            for i in range(1, 8):
                directions = [(rank + i, file + i), (rank - i, file + i), (rank + i, file - i),
                              (rank - i, file - i), (rank + i, file), (rank - i, file), (rank, file + i),
                              (rank, file - i)]
                for y, x in directions:
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        if board[y][x] is None:
                            pass
                        else:
                            if board[rank][file].isupper() != board[y][x].isupper() and directions.index(
                                    (y, x)) not in bannedDirections:
                                legalMoves.append((y, x))
                            bannedDirections.append(directions.index((y, x)))
                    else:
                        bannedDirections.append(directions.index((y, x)))

                directions = [i for i in directions if directions.index(i) not in bannedDirections]
                legalMoves += directions
        elif board[rank][file].upper() == 'K':
            bannedDirections = []
            directions = [(rank + 1, file + 1), (rank - 1, file + 1), (rank + 1, file - 1),
                          (rank - 1, file - 1), (rank + 1, file), (rank - 1, file), (rank, file + 1),
                          (rank, file - 1)]
            for y, x in directions:
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[y][x] is None:
                        pass
                    else:
                        if board[rank][file].isupper() != board[y][x].isupper():
                            legalMoves.append((y, x))
                        bannedDirections.append(directions.index((y, x)))
            directions = [i for i in directions if directions.index(i) not in bannedDirections]
            legalMoves += [i for i in directions if i not in generateLegalMovesForColor(board, board[rank][file].islower())]
    return legalMoves


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
        pos = pygame.Vector2(pygame.mouse.get_pos())
        image = pygame.image.load(pieceImages[selected_piece[0]])
        screen.blit(image, image.get_rect(center=pos))
        return y, x


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
                    legalMoves = generateLegalMovesForPiece(board, selected_piece[2], selected_piece[1])
                    if drop_pos in legalMoves:
                        piece, old_x, old_y = selected_piece
                        board[old_y][old_x] = None
                        new_y, new_x = drop_pos
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

import pygame
from copy import deepcopy
from pieceData import pieceImages

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

TILESIZE = 95
BOARD_POS = (580, 160)

moveHistory = []


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


def checkPossibleCastle(board, isWhite):
    possibleCastles = []
    rank = 7 * int(isWhite)
    if not any((rank, 4) in move for move in moveHistory) and board[rank][4] in ['K', 'k']:
        if not seeCheck(board, (rank, 4), (rank, 4), False):
            for i in range(2):
                if not any((rank, 7 * i) in move for move in moveHistory):
                    kingSquare = spotKing(board, isWhite)
                    if i:
                        squareRange = range(kingSquare[1]+1, 7)
                    else:
                        squareRange = range(1, kingSquare[1])
                    occupied = False
                    for j in squareRange:
                        if board[rank][j] is not None or seeCheck(board, (rank, 4), (rank, j), False):
                            occupied = True
                            break
                    if not occupied:
                        possibleCastles.append((rank, 7 * i))
    return possibleCastles


def makeCastleMove(board, rank, file):
    king = board[rank][4]
    rook = board[rank][file]
    board[rank][4] = None
    board[rank][file] = None
    if file < 1:
        board[rank][2] = king
        board[rank][3] = rook
    else:
        board[rank][6] = king
        board[rank][5] = rook


def checkEnPassant(board, rank, file):
    isWhite = board[rank][file].isupper()
    legalEnPassants = [(rank + 1*(-1)**int(isWhite), i) for i in range(file-1, file+2, 2) if i in range(0, 8) and moveHistory[-1] == [(rank + 2*(-1)**int(isWhite), i), (rank, file)]]
    return legalEnPassants


def seeCheck(board, before, after, isEnPassant):
    legalMoves = []
    newBoard = deepcopy(board)
    beforeSquare = board[before[0]][before[1]]
    newBoard[before[0]][before[1]] = None
    newBoard[after[0]][after[1]] = beforeSquare
    kingSquare = None
    for rank in range(8):
        for file in range(8):
            if type(newBoard[rank][file]) is str:
                if newBoard[rank][file].isupper() == newBoard[after[0]][after[1]].islower():
                    if newBoard[rank][file].upper() == 'R':
                        bannedDirections = []
                        for i in range(1, 8):
                            directions = [(rank + i, file), (rank - i, file), (rank, file + i), (rank, file - i)]
                            for y, x in directions:
                                if 0 <= x <= 7 and 0 <= y <= 7:
                                    if newBoard[y][x] is None:
                                        pass
                                    else:
                                        if directions.index((y, x)) not in bannedDirections:
                                            legalMoves.append((y, x))
                                        bannedDirections.append(directions.index((y, x)))
                                else:
                                    bannedDirections.append(directions.index((y, x)))

                            legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
                    elif newBoard[rank][file].upper() == 'B':
                        bannedDirections = []
                        for i in range(1, 8):
                            directions = [(rank + i, file + i), (rank - i, file + i), (rank + i, file - i),
                                          (rank - i, file - i)]
                            for y, x in directions:
                                if 0 <= x <= 7 and 0 <= y <= 7:
                                    if newBoard[y][x] is None:
                                        pass
                                    else:
                                        if directions.index((y, x)) not in bannedDirections:
                                            legalMoves.append((y, x))
                                        bannedDirections.append(directions.index((y, x)))
                                else:
                                    bannedDirections.append(directions.index((y, x)))

                            legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
                    elif newBoard[rank][file].upper() == 'Q':
                        bannedDirections = []
                        for i in range(1, 8):
                            directions = [(rank + i, file + i), (rank - i, file + i), (rank + i, file - i),
                                          (rank - i, file - i), (rank + i, file), (rank - i, file), (rank, file + i),
                                          (rank, file - i)]
                            for y, x in directions:
                                if 0 <= x <= 7 and 0 <= y <= 7:
                                    if newBoard[y][x] is None:
                                        pass
                                    else:
                                        if directions.index((y, x)) not in bannedDirections:
                                            legalMoves.append((y, x))
                                        bannedDirections.append(directions.index((y, x)))
                                else:
                                    bannedDirections.append(directions.index((y, x)))

                            legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
                    elif newBoard[rank][file].upper() == 'K':
                        bannedDirections = []
                        directions = [(rank + 1, file + 1), (rank - 1, file + 1), (rank + 1, file - 1),
                                      (rank - 1, file - 1), (rank + 1, file), (rank - 1, file), (rank, file + 1),
                                      (rank, file - 1)]
                        for y, x in directions:
                            if 0 <= x <= 7 and 0 <= y <= 7:
                                pass
                            else:
                                bannedDirections.append(directions.index((y, x)))
                        legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
                    elif newBoard[rank][file].upper() == 'N':
                        directions = [(rank + 2, file + 1), (rank + 2, file - 1), (rank - 2, file + 1),
                                      (rank - 2, file - 1), (rank + 1, file + 2), (rank + 1, file - 2),
                                      (rank - 1, file + 2), (rank - 1, file - 2)]
                        directions = [(y, x) for y, x in directions if (0 <= x <= 7) and (0 <= y <= 7)]
                        legalMoves += directions
                    elif newBoard[rank][file].upper() == 'P':
                        directions = []
                        if newBoard[rank][file].isupper():
                            if 0 <= rank - 1 <= 7:
                                if newBoard[rank - 1][file] is None:
                                    directions.append((rank - 1, file))
                                    if rank == 6 and newBoard[rank - 2][file] is None:
                                        directions.append((rank - 2, file))
                                for i in range(2):
                                    if 0 <= file + (-1) ** i <= 7:
                                        if newBoard[rank - 1][file + (-1) ** i] is not None:
                                            if newBoard[rank - 1][file + (-1) ** i].isupper() != newBoard[rank][file].isupper():
                                                directions.append((rank - 1, file + (-1) ** i))
                        else:
                            if 0 <= rank + 1 <= 7:
                                if newBoard[rank + 1][file] is None:
                                    directions.append((rank + 1, file))
                                    if rank == 1 and newBoard[rank + 2][file] is None:
                                        directions.append((rank + 2, file))
                                for i in range(2):
                                    if 0 <= file + (-1) ** i <= 7:
                                        if newBoard[rank + 1][file + (-1) ** i] is not None:
                                            if newBoard[rank + 1][file + (-1) ** i].isupper() != newBoard[rank][file].isupper():
                                                directions.append((rank + 1, file + (-1) ** i))
                        legalMoves += directions
    for rank in range(8):
        for file in range(8):
            if type(newBoard[rank][file]) is str:
                if newBoard[rank][file].isupper() == newBoard[after[0]][after[1]].isupper() and newBoard[rank][file].upper() == 'K':
                    kingSquare = (rank, file)
                    break
        if kingSquare is not None:
            break
    return kingSquare in legalMoves


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

                legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
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

                legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
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

                legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
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
                else:
                    bannedDirections.append(directions.index((y, x)))
            legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
            if (rank == 0 or rank == 7) and file == 4:
                legalMoves += checkPossibleCastle(board, board[rank][file].isupper())
        elif board[rank][file].upper() == 'N':
            bannedDirections = []
            directions = [(rank + 2, file + 1), (rank + 2, file - 1), (rank - 2, file + 1),
                          (rank - 2, file - 1), (rank + 1, file + 2), (rank + 1, file - 2), (rank - 1, file + 2),
                          (rank - 1, file - 2)]
            for y, x in directions:
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[y][x] is None:
                        pass
                    else:
                        if board[rank][file].isupper() != board[y][x].isupper():
                            legalMoves.append((y, x))
                        bannedDirections.append(directions.index((y, x)))
                else:
                    bannedDirections.append(directions.index((y, x)))
            legalMoves += [i for i in directions if directions.index(i) not in bannedDirections]
        elif board[rank][file].upper() == 'P':
            directions = []
            if (board[rank][file].isupper() and rank == 3) or (board[rank][file].islower() and rank == 5):
                legalMoves += checkEnPassant(board, rank, file)
            if board[rank][file].isupper():
                if 0 <= rank - 1 <= 7:
                    if board[rank - 1][file] is None:
                        directions.append((rank - 1, file))
                        if rank == 6 and board[rank - 2][file] is None:
                            directions.append((rank - 2, file))
                    if 0 <= file - 1 <= 7:
                        if board[rank - 1][file - 1] is not None:
                            if board[rank][file].isupper() != board[rank - 1][file - 1].isupper():
                                directions.append((rank - 1, file - 1))
                    if 0 <= file + 1 <= 7:
                        if board[rank - 1][file + 1] is not None:
                            if board[rank][file].isupper() != board[rank - 1][file + 1].isupper():
                                directions.append((rank - 1, file + 1))
            else:
                if 0 <= rank + 1 <= 7:
                    if board[rank + 1][file] is None:
                        directions.append((rank + 1, file))
                        if rank == 1 and board[rank + 2][file] is None:
                            directions.append((rank + 2, file))
                    if 0 <= file - 1 <= 7:
                        if board[rank + 1][file - 1] is not None:
                            if board[rank][file].isupper() != board[rank + 1][file - 1].isupper():
                                directions.append((rank + 1, file - 1))
                    if 0 <= file + 1 <= 7:
                        if board[rank + 1][file + 1] is not None:
                            if board[rank][file].isupper() != board[rank + 1][file + 1].isupper():
                                directions.append((rank + 1, file + 1))
            legalMoves += directions
        legalMoves = [i for i in legalMoves if not seeCheck(board, (rank, file), i, False)]
    return legalMoves


def generateLegalMovesForColor(board, isWhite):
    legalMoves = []
    for rank in range(8):
        for file in range(8):
            if board[rank][file] is not None:
                if board[rank][file].isupper() == isWhite:
                    legalMoves += generateLegalMovesForPiece(board, rank, file)
    return legalMoves


def spotKing(board, isWhite):
    for rank in range(8):
        for file in range(8):
            if board[rank][file] is not None:
                if board[rank][file].isupper() == isWhite and board[rank][file].upper() == 'K':
                    return rank, file


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
    font = pygame.font.SysFont('', 32)
    screen = pygame.display.set_mode((1920, 1000))
    board = create_board()
    loadFromFEN(startingFen, board)
    board_surf = create_board_surf()
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    whitesTurn = True
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
                    if selected_piece[0].isupper() == whitesTurn:
                        legalMoves = generateLegalMovesForPiece(board, selected_piece[2], selected_piece[1])
                        if drop_pos in legalMoves:
                            if drop_pos in checkPossibleCastle(board, whitesTurn):
                                makeCastleMove(board, drop_pos[0], drop_pos[1])
                            else:
                                piece, old_x, old_y = selected_piece
                                board[old_y][old_x] = None
                                new_y, new_x = drop_pos
                                board[new_y][new_x] = piece
                                moveHistory.append([(old_y, old_x), (new_y, new_x)])
                            whitesTurn = not whitesTurn
                selected_piece = None
                drop_pos = None

        if len(generateLegalMovesForColor(board, whitesTurn)) == 0:
            if spotKing(board, whitesTurn) in generateLegalMovesForColor(board, not whitesTurn):
                endText = font.render('Checkmate! Black has won!' if whitesTurn else 'Checkmate! White has won!', True,
                                      'black')
            else:
                endText = font.render("Stalemate! It's a draw!", True, 'black')
            textRect = endText.get_rect()
            textRect.center = (1920 // 2, 1000 // 2)
            screen.blit(endText, textRect)
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

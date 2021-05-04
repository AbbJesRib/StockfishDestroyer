import pygame
from pieceData import pieceImages
from chessRules import moveHistory, checkEnPassant, checkPossibleCastle, generateLegalMovesForColor, generateLegalMovesForPiece, makeCastleMove, spotKing

startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

TILESIZE = 95
BOARD_POS = (580, 160)

boardHistory = [startingFen]

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


def loadFENFromBoard(board):
    fen = ''
    for rank in range(8):
        spaceBetween = 0
        for file in range(8):
            if board[rank][file] is not None:
                if spaceBetween != 0:
                    fen += str(spaceBetween)
                    spaceBetween = 0
                fen += board[rank][file]
            else:
                spaceBetween += 1
        if spaceBetween != 0:
            fen += str(spaceBetween)
        fen += '/'
    fen = fen[:-1]
    return fen


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
    gameEnd = False
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
                                try:
                                    if drop_pos in checkEnPassant(board, selected_piece[2], selected_piece[1]):
                                        board[selected_piece[2]][drop_pos[1]] = None
                                except IndexError:
                                    pass
                                piece, old_x, old_y = selected_piece
                                board[old_y][old_x] = None
                                new_y, new_x = drop_pos
                                board[new_y][new_x] = piece
                                moveHistory.append([(old_y, old_x), (new_y, new_x)])
                            boardHistory.append(loadFENFromBoard(board))
                            whitesTurn = not whitesTurn
                selected_piece = None
                drop_pos = None
                if len(generateLegalMovesForColor(board, whitesTurn)) == 0:
                    gameEnd = True
                    if spotKing(board, whitesTurn) in generateLegalMovesForColor(board, not whitesTurn):
                        endText = font.render('Checkmate! Black has won!' if whitesTurn else 'Checkmate! White has won!', True,
                                              'black')
                    else:
                        endText = font.render("Stalemate! It's a draw!", True, 'black')
                    textRect = endText.get_rect()
                    textRect.center = (1920 // 2, 1000 // 2)
                    screen.blit(endText, textRect)
                if boardHistory.count(boardHistory[-1]) == 3:
                    gameEnd = True

        screen.fill(pygame.Color('black'))
        screen.blit(board_surf, BOARD_POS)
        draw_pieces(screen, board, selected_piece)
        if not gameEnd:
            draw_selector(screen, piece, x, y)
            drop_pos = draw_drag(screen, board, selected_piece)

        if x is not None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()

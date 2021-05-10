import pygame
from pieceData import pieceImages
from chessRules import generateLegalMovesForColor, spotKing, endTurn, moveHistory
from chessAI import search, minimax, alphaBetaPruning, evaluate


TILESIZE = 95
BOARD_POS = (580, 160)


def Square(square):
    rank, file = square
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return f"{letters[file]}{8-rank}"


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
    screen = pygame.display.set_mode((1920, 1000))
    onStartScreen = True
    playerisWhite = True
    while onStartScreen:
        screen.fill((0, 0, 0))
        myfont = pygame.font.SysFont("Britannic Bold", 40)
        text1 = myfont.render("Left click for white", 1, (255, 0, 0))
        text2 = myfont.render("Right click for black", 1, (255, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    playerisWhite = False
                onStartScreen = False
        screen.blit(text1, (200, 200))
        screen.blit(text2, (200, 300))
        pygame.display.flip()
    font = pygame.font.SysFont('', 32)
    board = create_board()
    startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    boardHistory = [startingFen]
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
        if not gameEnd:
            # if len(generateLegalMovesForColor(board, whitesTurn)) == 0:
            #     gameEnd = True
            #     kingPos = spotKing(board, whitesTurn)
            #     inCheck = False
            #     if len([i for i in generateLegalMovesForColor(board, not whitesTurn) if i[1] == kingPos]):
            #         inCheck = True
            #     if not inCheck:
            #         print("Stalemate! It's a draw!")
            #     else:
            #         print("Checkmate! Black has won!" if whitesTurn else "Checkmate! White has won!")
            if boardHistory.count(boardHistory[-1]) == 3:
                print("It's a draw by repetition!")
                gameEnd = True

            if whitesTurn != playerisWhite and not gameEnd:
                # print(search(board, 2, not playerisWhite, float('-inf'), float('inf'), playerisWhite))
                move = search(board, 1, not playerisWhite, moveHistory)
                whitesTurn = endTurn(board, move[0], move[1], not playerisWhite, whitesTurn, move[2], boardHistory)

        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if piece is not None:
                    selected_piece = piece, x, y
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    if selected_piece[0].isupper() == whitesTurn:
                        # print(evaluate(board, not playerisWhite))
                        whitesTurn = endTurn(board, (selected_piece[2], selected_piece[1]), drop_pos, playerisWhite, whitesTurn, None, boardHistory)
                        # print(evaluate(board, playerisWhite))
                selected_piece = None
                drop_pos = None

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

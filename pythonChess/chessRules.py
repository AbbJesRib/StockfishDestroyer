from copy import deepcopy
moveHistory = []


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
    legalEnPassants = [(rank + 1*(-1)**int(isWhite), i) for i in range(file-1, file+2, 2) if i in range(0, 8) and moveHistory[-1] == [(rank + 2*(-1)**int(isWhite), i), (rank, i)]]
    legalEnPassants = [i for i in legalEnPassants if not seeCheck(board, (rank, file), i, True)]
    return legalEnPassants


def seeCheck(board, before, after, isEnPassant):
    legalMoves = []
    newBoard = deepcopy(board)
    beforeSquare = board[before[0]][before[1]]
    newBoard[before[0]][before[1]] = None
    newBoard[after[0]][after[1]] = beforeSquare
    kingSquare = None
    if isEnPassant:
        newBoard[before[0]][after[1]] = None
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
            legalMoves += [i for i in directions if not seeCheck(board, (rank, file), i, False)]
            if (board[rank][file].isupper() and rank == 3) or (board[rank][file].islower() and rank == 4):
                legalMoves += checkEnPassant(board, rank, file)
        if board[rank][file].upper() != 'P':
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
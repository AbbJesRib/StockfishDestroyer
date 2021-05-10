from chessRules import moveHistory, checkEnPassant, checkPossibleCastle, generateLegalMovesForColor, \
    generateLegalMovesForPiece, seeCheck, makeCastleMove, spotKing, makeMove
import random
from copy import deepcopy
from pieceData import pieceValue
from time import time


def sortMoves(board, isWhite, movesMade):
    moves = generateLegalMovesForColor(board, isWhite)
    sortedMoves = []
    for before, after, AIProm in moves:
        move = (before, after, AIProm)
        piece = board[before[0]][before[1]]
        capturedPiece = board[after[0]][after[1]]
        newBoard = deepcopy(board)
        history = deepcopy(movesMade)
        makeMove(newBoard, before, after, AIProm, history)
        if board[before[0]][before[1]].upper != 'K':
            if capturedPiece is not None:
                if abs(pieceValue[capturedPiece]) > abs(pieceValue[piece]):
                    sortedMoves.insert(0, move)
                    continue
                elif (after[0], after[1], any(['Q', 'R', 'B', 'N', 'q', 'r', 'b', 'n', None])) not in generateLegalMovesForColor(newBoard, not isWhite):
                    sortedMoves.insert(0, move)
                    continue
                else:
                    sortedMoves.insert(int(len(sortedMoves)/2), move)
                    continue
        if spotKing(board, not isWhite) in generateLegalMovesForColor(newBoard, isWhite):
            sortedMoves.insert(0, move)
            continue
        if (after[0], after[1], any(['Q', 'R', 'B', 'N', 'q', 'r', 'b', 'n', None])) in generateLegalMovesForColor(newBoard, not isWhite):
            sortedMoves.insert(len(sortedMoves)-1, move)
            continue
        sortedMoves.insert(int(len(sortedMoves)/2), move)
    return sortedMoves


def Square(square):
    rank, file = square
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return f"{letters[file]}{8-rank}"


def makeRandomMove(board, isWhite):
    legalMoves = generateLegalMovesForColor(board, isWhite)
    move = random.choice(legalMoves)
    return move


def countMaterial(board, isWhite):
    material = 0
    for piece in pieceValue.keys():
        if piece.isupper() == isWhite:
            material += sum(rank.count(piece) for rank in board) * pieceValue[piece]
    return material


def evaluate(board, isWhite):
    # whiteMaterial = countMaterial(board, True)
    # blackMaterial = countMaterial(board, False)

    # return (blackMaterial - whiteMaterial)*(-1)**int(isWhite)
    material = 0
    for piece in pieceValue.keys():
        material += sum(rank.count(piece) for rank in board) * pieceValue[piece]

    return material * (-1) ** int(not isWhite)


def minimax(board, depth, isWhite, movesMade):
    if depth == 0:
        return evaluate(board, isWhite)

    legalMoves = generateLegalMovesForColor(board, isWhite)
    if len(legalMoves) == 0:
        kingSquare = spotKing(board, isWhite)
        if seeCheck(board, kingSquare, kingSquare, False):
            return float('-inf')
        return 0

    bestEval = float('-inf')

    for before, after, AIProm in legalMoves:
        newBoard = deepcopy(board)
        movesMade = deepcopy(movesMade)
        makeMove(newBoard, before, after, AIProm, movesMade)
        evaluation = -minimax(board, depth-1, not isWhite, movesMade)
        bestEval = max(evaluation, bestEval)

    return bestEval


# def alphaBetaPruning(board, depth, maximizingPlayer, alpha, beta, playerisWhite, movesMade):
#     if depth == 0:
#         return evaluate(board, maximizingPlayer != playerisWhite)
#     legalMoves = generateLegalMovesForColor(board, maximizingPlayer != playerisWhite)  # Generates all legal moves this player can make
#     if len(legalMoves) == 0:  # When the current player has no available moves
#         kingSquare = spotKing(board, maximizingPlayer != playerisWhite)
#         if seeCheck(board, kingSquare, kingSquare, False):
#             return float('-inf')  # Returns negative infinity if the player is in check
#         return 0  # Otherwise (stalemate) it returns 0
#
#     if maximizingPlayer:
#         value = float('-inf')
#         for before, after, AIProm in legalMoves:  # Goes through every move
#             newBoard = deepcopy(board)  # Creates a new copy of the board
#             history = deepcopy(movesMade)
#             makeMove(newBoard, before, after, AIProm, history)  # Makes the move on the new copy
#             value = max(value, alphaBetaPruning(newBoard, depth - 1, False, alpha, beta, playerisWhite, history))  # Searches the copy of the board but for the opponent
#             alpha = max(alpha, value)
#             if alpha >= beta:
#                 break
#         return value
#     else:
#         value = float('inf')
#         for before, after, AIProm in legalMoves:  # Goes through every move
#             newBoard = deepcopy(board)  # Creates a new copy of the board
#             makeMove(newBoard, before, after, AIProm, history)  # Makes the move on the new copy
#             value = min(value, alphaBetaPruning(newBoard, depth - 1, True, alpha, beta, playerisWhite, history))  # Searches the copy of the board but for the opponent
#             beta = min(beta, value)
#             if alpha >= beta:
#                 break
#         return value

def alphaBetaPruning(board, depth, isWhite, alpha, beta, movesMade):
    if depth == 0:
        return evaluate(board, isWhite)
    legalMoves = generateLegalMovesForColor(board, isWhite)  # Generates all legal moves this player can make
    if len(legalMoves) == 0:  # When the current player has no available moves
        kingSquare = spotKing(board, isWhite)
        if seeCheck(board, kingSquare, kingSquare, False):
            return float('-inf')  # Returns negative infinity if the player is in check
        return 0

    for before, after, AIProm in legalMoves:
        newBoard = deepcopy(board)
        history = deepcopy(movesMade)
        makeMove(newBoard, before, after, AIProm, history)
        evaluation = -alphaBetaPruning(board, depth-1, not isWhite, -beta, -alpha, history)
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
    return alpha


def search(board, depth, isWhite, movesMade):
    bestEval = float('-inf')
    bestMove = None
    legalMoves = generateLegalMovesForColor(board, isWhite)

    for before, after, AIProm in legalMoves:
        move = (before, after, AIProm)
        newBoard = deepcopy(board)
        history = deepcopy(movesMade)
        makeMove(newBoard, before, after, AIProm, history)
        value = -alphaBetaPruning(newBoard, depth-1, not isWhite, float('-inf'), float('inf'), history)
        # value = -minimax(newBoard, depth-1, not isWhite, history)
        if value >= bestEval:
            bestEval = value
            bestMove = move

    return bestMove


from chessRules import moveHistory, checkEnPassant, checkPossibleCastle, generateLegalMovesForColor, generateLegalMovesForPiece, seeCheck, makeCastleMove, spotKing, makeMove
import random
from copy import deepcopy
from pieceData import pieceValue


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

    return material*(-1)**int(not isWhite)


def search(board, depth, isWhite, alpha, beta):
    print(depth)
    if depth == 0:
        return evaluate(board, isWhite)
    legalMoves = generateLegalMovesForColor(board, isWhite)
    if len(legalMoves) == 0:
        if seeCheck(board, spotKing(board, isWhite), spotKing(board, isWhite), False):
            return float('-inf')
        return 0

    print('searching through every possible move at depth', depth)
    for before, after, AIProm in legalMoves:
        newBoard = deepcopy(board)
        makeMove(newBoard, before, after, AIProm)
        evaluation = -search(board, depth-1, not isWhite, -alpha, -beta)
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)

    return alpha

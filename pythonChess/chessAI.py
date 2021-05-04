from chessRules import moveHistory, checkEnPassant, checkPossibleCastle, generateLegalMovesForColor, generateLegalMovesForPiece, makeCastleMove, spotKing
import random
from pieceData import pieceValue


def makeRandomMove(board, isWhite):
    legalMoves = generateLegalMovesForColor(board, isWhite)
    move = random.choice(legalMoves)
    return move


def evaluateBoard(board):
    evaluation = 0
    for rank in range(8):
        for file in range(8):
            if board[rank][file] is not None:
                evaluation += pieceValue[board[rank][file]]
    return evaluation
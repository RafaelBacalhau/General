from player import Player
import math
import copy
import cProfile, pstats
from io import StringIO
import utils

class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """
	
    def __init__(self):
        self.name = "Mettez ici le nom de votre IA"

    def scorePosition(self, board, row, column, dy, dx):
        my_points = 0
        for i in range(0,4):
            if board.getCol(column)[5-row] == self.color:
                my_points+=1
            row += dy
            column += dx
        else:
            return my_points

    def heuristics(self, board):
        points = 0
        for row in range(0,6):
            for column in range(0,7):
                if(row < 3):
                    score = self.scorePosition(board, row, column, 1, 0)
                    points += score
                    if(column < 4):
                        score = self.scorePosition(board, row, column, 1, 1)
                        points += score

                if(column < 4):
                    score = self.scorePosition(board, row, column, 0, 1)
                    points += score
                    if(row >= 3):
                        score = self.scorePosition(board, row, column, -1, 1)
                        points += score

        return points

    def max(self, board, depth, alpha = -math.inf, beta=math.inf, coords_last_play=(-1,-1)):
        result = self.getWinner(board, coords_last_play)
        if (result == 1 or result == -1):
            return (None, self.color * result * 100000 - 4-depth*result)
        if (board.isFull()):
            return (None, 0)

        if depth == 0:
            # HEURISTICS
            return (None, self.heuristics(board))

        final_column = (None, -99999)
        for column in board.getPossibleColumns():
            newBoard = copy.deepcopy(board)
            row = newBoard.play(self.color, column)

            nextMove = self.min(newBoard, depth -1, alpha, beta, (column, row))

            if(final_column[0] == None or nextMove[1] > final_column[1]):
                final_column = (column, nextMove[1])
                alpha = nextMove[1]
            print("Value for max: depth " + str(depth) + ", column " + str(column) + " = " + str(final_column))
            print(newBoard)
            if (alpha >= beta):
                return final_column

        return final_column



    def min(self, board, depth, alpha=-math.inf, beta=math.inf, coords_last_play=(-1,-1)):
        result = self.getWinner(board, coords_last_play)
        if(result == 1 or result == -1):
            return (None, self.color * result * 100000- 4-depth*result)
        if(board.isFull()):
            return (None, 0)

        if depth == 0 :
            # HEURISTICS
            return (None, self.heuristics(board))

        final_column = (None, 99999)
        for column in board.getPossibleColumns():
            #print(column)
            newBoard = copy.deepcopy(board)
            row = newBoard.play(-self.color, column)

            nextMove = self.max(newBoard, depth-1, alpha, beta, (column, row))

            if (final_column[0] == None or nextMove[1] < final_column[1]):
                final_column = (column, nextMove[1])
                beta = nextMove[1]
            print("Value for min: depth " + str(depth) + ", column " + str(column) + " = " + str(final_column))
            print(newBoard)
            if (alpha >= beta):
                return final_column

        return final_column


    def getColumn(self, board):
         # TODO(student): implement this!
         #pr = cProfile.Profile()
         #pr.enable()
         if(board.getRow(0) == [0,0,0,0,0,0,0]):
             column_to_choose = (3,0)
         else:
             column_to_choose = self.max(board, 4, coords_last_play=(0,0))
         #pr.disable()
         #s = StringIO()
         #sortby = 'cumulative'
         #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
         #ps.print_stats()
         #print(s.getvalue())
         print("******************************************")
         return column_to_choose[0]

    def getWinner(self, board, pos):
        """Returns the player (boolean) who won, or None if nobody won"""
        tests = []
        tests.append(board.getCol(pos[0]))
        tests.append(board.getRow(pos[1]))
        tests.append(board.getDiagonal(True, pos[0] - pos[1]))
        tests.append(board.getDiagonal(False, pos[0] + pos[1]))
        for test in tests:
            color, size = utils.longest(test)
            if size >= 4:
                return color


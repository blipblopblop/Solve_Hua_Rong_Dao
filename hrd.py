from copy import deepcopy
from heapq import heapify, heappush, heappop
import time
import argparse
import sys

#====================================================================================

char_goal = '1'
char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    # print out the attributes of a piece for debugging
    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)

    # USELESS
    # move a piece 
    # check legality prior to calling 
    def move(self, x, y):
        # move is + or - 1 
        self.coord_x += x
        self.coord_y += y


class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """
        # board size is static
        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()

    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'
                    '''if ( (piece.coord_y + 1, piece.coord_x) == (4, 0)):
                        #self.display()
                        #print('\n')'''

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                if ch != None:
                    print(ch, end='')
                
            print()
        
        return 1
    
    # find the two empty spaces on the board
    # use pg 3/7 bottom half to help you with this
    def find_empty(self):
        empty = []
        col = 0
        for i, line in enumerate(self.grid):
            for ch in line:
                if ch == '.':
                    empty.append((i, col))
                col += 1
            col = 0
        # list of tuple for each '.' position
        return empty

    # all plausible moves
    def legality(self):
        loc_e = self.find_empty()
        sp1 = (loc_e[0][0], loc_e[0][1])
        sp2 = (loc_e[1][0], loc_e[1][1])
        legal_moves = []
        #print("135")

        # space is horizantal and beside each other
        if ((sp1[0] == sp2[0]) and (abs(sp1[1] - sp2[1]) == 1)):
            # 4 by 4 (holds for when spaces are also not beside each other)
            # check spaces are beside
            # Goal is above
            if (((sp1[0] - 2 >= 0) and (sp2[0] - 2 >= 0))) and (((self.grid[sp1[0] - 1][sp1[1]] == char_goal) and (self.grid[sp2[0] - 1][sp2[1]] == char_goal)) and ((self.grid[sp1[0] - 2][sp1[1]] == char_goal) and (self.grid[sp2[0] - 2][sp2[1]] == char_goal))):
                legal_moves.append(([(sp1[0] - 2, sp1[1]), (sp2[0] - 2, sp2[1])], char_goal, 2, [sp1, sp2], "x"))
            # Goal is below
            if (((sp1[0] + 2 < 5) and (sp2[0] + 2 < 5))) and (((self.grid[sp1[0] + 1][sp1[1]] == char_goal) and (self.grid[sp2[0] + 1][sp2[1]] == char_goal)) and ((self.grid[sp1[0] + 2][sp1[1]] == char_goal) and (self.grid[sp2[0] + 2][sp2[1]] == char_goal))):
                legal_moves.append(([(sp1[0] + 2, sp1[1]), (sp2[0] + 2, sp2[1])], char_goal, 2, [sp1, sp2], "x"))
            
            # 2 by 1 
            # for RHS empty 
            # --<>
            if (sp1[1] + 2 < 4 and sp2[1] + 2 < 4) and (self.grid[sp1[0]][sp1[1] + 2] == '<' and self.grid[sp2[0]][sp2[1] + 2] == '>'):
                #print("\n 155")
                legal_moves.append((([(sp1[0], sp1[1] + 2), (sp2[0], sp2[1] + 2)]), '<>', 2, [sp1, sp2], "y"))
            # for LHS empty
            # <>--
            #print("150")
            if (sp1[1] - 2 >= 0 and sp2[1] - 2 >= 0) and (self.grid[sp1[0]][sp1[1] - 2] == '<' and self.grid[sp2[0]][sp2[1] - 2] == '>'):
                #print("\n 151")
                legal_moves.append((([(sp1[0], sp1[1] - 2), (sp2[0], sp2[1] - 2)]), '<>', 2, [sp1, sp2], "y"))
                #self.display()
            # for bottom push
            # --
            # <> 
            if (sp1[0] + 1 < 5 and sp2[0] + 1 < 5) and (self.grid[sp1[0] + 1][sp1[1]] == '<' and self.grid[sp2[0] + 1][sp2[1]] == '>'):
                #print("\n 155")
                legal_moves.append((([(sp1[0] + 1, sp1[1]), (sp2[0] + 1, sp2[1])]), '<>', 2, [sp1, sp2], "x"))
            # for top push 
            # <>
            # --
            if (sp1[0] - 1 >= 0 and sp2[0] - 1 >= 0) and (self.grid[sp1[0] - 1][sp1[1]] == '<' and self.grid[sp2[0] - 1][sp2[1]] == '>'):
                #print("\n 155")
                legal_moves.append((([(sp1[0] - 1, sp1[1]), (sp2[0] - 1, sp2[1])]), '<>', 2, [sp1, sp2], "x"))

        # space is vertical
        # sp1 is above sp2 or sp1 is below sp2
        if (abs(sp1[0] - sp2[0]) == 1) and (sp1[1] == sp2[1]):           
            # 4 by 4
            # check spaces are beside
            # Goal is above
            if ((sp1[1] - 1 >= 0) and (sp2[1] - 2 >= 0)) and (((self.grid[sp1[0]][sp1[1] - 1] == char_goal) and (self.grid[sp2[0]][sp2[1] - 1] == char_goal)) and ((self.grid[sp1[0]][sp1[1] - 2] == char_goal) and (self.grid[sp2[0]][sp2[1] - 2] == char_goal))):
                legal_moves.append(([(sp1[0], sp1[1] - 2), (sp2[0], sp2[1] - 2)], char_goal, 2, [sp1, sp2], "y"))
            # Goal is below
            if ((sp1[1] + 1 < 4) and (sp2[1] + 2 < 4)) and (((self.grid[sp1[0]][sp1[1] + 1] == char_goal) and (self.grid[sp2[0]][sp2[1] + 1] == char_goal)) and ((self.grid[sp1[0]][sp1[1] + 2] == char_goal) and (self.grid[sp2[0]][sp2[1] + 2] == char_goal))):
                legal_moves.append(([(sp1[0], sp1[1] + 2), (sp2[0], sp2[1] + 2)], char_goal, 2, [sp1, sp2], "y"))

            # 1 by 2 
            # for LHS empty
            # ^ -
            # v -
            if (sp1[1] - 1 >= 0 and sp2[1] - 1 >= 0) and ((self.grid[sp1[0]][sp1[1] - 1] == '^') and (self.grid[sp2[0]][sp2[1] - 1] == 'v')):
                legal_moves.append(([(sp1[0], sp1[1] - 1),(sp2[0], sp2[1] - 1)],'^v', 2, [sp1, sp2], "y"))
            # for RHS empty 
            # - ^
            # - v
            if (sp1[1] + 1 < 4 and sp2[1] + 1 < 4) and (self.grid[sp1[0]][sp1[1] + 1] == '^' and self.grid[sp2[0]][sp2[1] + 1] == 'v'):
                legal_moves.append(([(sp1[0], sp1[1] + 1),(sp2[0], sp2[1] + 1)],'^v', 2, [sp1, sp2], "y"))
            # for bottom push
            # -
            # -
            # ^
            # v
            #if (sp1[0] + 2 < 5 and sp2[0] + 2 < 5) and (self.grid[sp1[0] + 2][sp1[1]] == '^' and self.grid[sp2[0] + 2][sp2[1]] == 'v'):
                #legal_moves.append(([(sp1[0] + 2, sp1[1]),(sp2[0] + 2, sp2[1])],'^v', 2, [sp1, sp2], "x"))
            # for top push
            # ^
            # v
            # -
            # -
            #if (sp1[0] - 2 >= 0 and sp2[0] - 2 >= 0) and (self.grid[sp1[0] - 2][sp1[1]] == '^' and self.grid[sp2[0] - 2][sp2[1]] == 'v'):
                #legal_moves.append(([(sp1[0] - 2, sp1[1]),(sp2[0] - 2, sp2[1])],'^v', 2, [sp1, sp2], "x"))
        
        # 2 by 1 and Singles (holds for when spaces are not beside each other)
        # -<> is on the right
        if (sp1[1] + 1 < 4 and sp1[1] + 2 < 4) and (self.grid[sp1[0]][sp1[1] + 1] == '<' and self.grid[sp1[0]][sp1[1] + 2] == '>'):
            legal_moves.append(([(sp1[0], sp1[1] + 1),(sp1[0], sp1[1] + 2)],'<>', 1, [sp1], "x"))
        # -<> is on the right
        if (sp2[1] + 1 < 4 and sp2[1] + 2 < 4) and (self.grid[sp2[0]][sp2[1] + 1] == '<' and self.grid[sp2[0]][sp2[1] + 2] == '>'):
            legal_moves.append(([(sp2[0], sp2[1] + 1),(sp2[0], sp2[1] + 2)],'<>', 1, [sp2], "x"))   
        # for LHS empty 
        if (sp2[1] - 1 >= 0 and sp2[1] - 2 >= 0) and (self.grid[sp2[0]][sp2[1] - 1] == '>' and self.grid[sp2[0]][sp2[1] - 2] == '>'):
            legal_moves.append(([(sp2[0], sp2[1] - 1),(sp2[0], sp2[1] - 2)],'<>', 1, [sp2], "x"))
        # for LHS empty
        # <>- on the left
        if (sp1[1] - 1 >= 0 and sp1[1] - 2 >= 0) and (self.grid[sp1[0]][sp1[1] - 1] == '>' and self.grid[sp1[0]][sp1[1] - 2] == '>'):
            legal_moves.append(([(sp1[0], sp1[1] - 1),(sp1[0], sp1[1] - 2)],'<>', 1, [sp1], "x"))     

        # spaces are not together  
        # 1 by 2 (holds for when spaces are not beside each other)
        # for LHS empty
        # ^
        # v is above
        # -
        if (sp1[0] - 1 >= 0 and sp1[0] - 2 >= 0) and (self.grid[sp1[0] - 1][sp1[1]] == 'v' and self.grid[sp1[0] - 2][sp1[1]] == '^'):           
            #input()
            #print("lINE 185", sp1)
            #self.display()
            #self.display()
            legal_moves.append(([(sp1[0] - 1, sp1[1]),(sp1[0] - 2, sp1[1])],'^v', 1, [sp1], "x"))
            #print('\n', self.grid[sp1[0] - 1][sp1[1]], self.grid[sp1[0] - 2][sp1[1]], '\n')
        # -
        # ^
        # v is below
        if (sp1[0] + 1 < 5 and sp1[0] + 2 < 5) and (self.grid[sp1[0] + 1][sp1[1]] == '^' and self.grid[sp1[0] + 2][sp1[1]] == 'v'):
            #print("lINE 188 HERE ERROR?")
            legal_moves.append(([(sp1[0] + 1, sp1[1]),(sp1[0] + 2, sp1[1])],'^v', 1, [sp1], "x"))
        # ^
        # v is above
        # -
        if (sp2[0] - 1 >= 0 and sp2[0] - 2 >= 0) and (self.grid[sp2[0] - 1][sp2[1]] == 'v' and self.grid[sp2[0] - 2][sp2[1]] == '^'):
            #print("lINE 192")
            '''print(sp2)'''
            legal_moves.append(([(sp2[0] - 1, sp2[1]),(sp2[0] - 2, sp2[1])],'^v', 1, [sp2], "y"))
            #print(self.grid[sp2[0] - 1][sp2[1]], self.grid[sp2[0] - 2][sp2[1]])
        # -
        # ^
        # v is below
        if (sp2[0] + 1 < 5 and sp2[0] + 2 < 5) and (self.grid[sp2[0] + 1][sp2[1]] == '^' and self.grid[sp2[0] + 2][sp2[1]] == 'v'):
            #print("lINE 197")
            legal_moves.append(([(sp2[0] + 1, sp2[1]),(sp2[0] + 2, sp2[1])],'^v', 1, [sp2], "y"))

        # single
        if (sp1[0] - 1 >= 0) and (self.grid[sp1[0] - 1][sp1[1]] == char_single):
            legal_moves.append(([(sp1[0] - 1, sp1[1])], char_single, 1, [sp1], "x"))
        if (sp1[0] + 1 < 5) and (self.grid[sp1[0] + 1][sp1[1]] == char_single):
            legal_moves.append(([(sp1[0] + 1, sp1[1])], char_single, 1, [sp1], "x"))
        if (sp1[1] - 1 >= 0) and (self.grid[sp1[0]][sp1[1] - 1] == char_single):
            legal_moves.append(([(sp1[0], sp1[1] - 1)], char_single, 1, [sp1], "y"))
        if (sp1[1] + 1 < 4) and self.grid[sp1[0]][sp1[1] + 1] == char_single:
            legal_moves.append(([(sp1[0], sp1[1] + 1)], char_single, 1, [sp1], "y"))
        if (sp2[0] - 1 >= 0) and (self.grid[sp2[0] - 1][sp2[1]] == char_single):
            legal_moves.append(([(sp2[0] - 1, sp2[1])], char_single, 1, [sp2], "x"))  
        if (sp2[0] + 1 < 5) and (self.grid[sp2[0] + 1][sp2[1]] == char_single):
            legal_moves.append(([(sp2[0] + 1, sp2[1])], char_single, 1, [sp2], "x"))    
        if (sp2[1] - 1 >= 0) and (self.grid[sp2[0]][sp2[1] - 1] == char_single):
            legal_moves.append(([(sp2[0], sp2[1] - 1)], char_single, 1, [sp2], "y"))    
        if (sp2[1] + 1 < 4) and (self.grid[sp2[0]][sp2[1] + 1] == char_single):
            legal_moves.append(([(sp2[0], sp2[1] + 1)], char_single, 1, [sp2], "y"))          
    
        return legal_moves
    

    # check if the goal peice is at the bottom opening [(4,1), (4,2)]
    def goal_test(self):
        col = 0
        goal_pos = []
        # find the goal piece
        for i, line in enumerate(self.grid):
            for ch in line:
                if ch == "1":
                    goal_pos.append((i, col))
                col += 1
            col = 0
        if goal_pos == [(3, 1), (3, 2), (4, 1), (4, 2)]:
            return True
        return False 
                    

# successor function
# change board configuration per space
# func calling this should call this twice
def change_board(move, changed_board, board):

    # make the board to change a copy of the current board
    for x in range(len(board.grid)):
        for y in range(len(board.grid[x])):
            if board.grid[x][y] != changed_board.grid[x][y]:
                changed_board.grid[x][y] = board.grid[x][y]

    #print(move, len(move[-2]), len(move[-5]))
    if len(move[-2]) > 1:   # spaces
        sp1 = move[-2][0]
        sp2 = move[-2][1]
        if len(move[-5]) > 1:   # num of piece's on grid spot
            pos = move[-5]
            p_mov = move[-4]
            if p_mov == char_goal:
                if (pos[0][0] == sp1[0] - 2) and (pos[0][1] == sp1[1]) and (pos[1][0] == sp2[0] - 2) and (pos[1][1] == sp2[1]):     # push 2 by 2 down
                    changed_board.grid[sp1[0] - 2][sp1[1]] = '.'
                    changed_board.grid[sp2[0] - 2][sp2[1]] = '.'
                    changed_board.grid[sp1[0] - 1][sp1[1]] = char_goal
                    changed_board.grid[sp2[0] - 1][sp2[1]] = char_goal
                    changed_board.grid[sp1[0]][sp1[1]] = char_goal
                    changed_board.grid[sp2[0]][sp2[1]] = char_goal
                    return changed_board
                elif (pos[0][0] == sp1[0] + 2) and (pos[0][1] == sp1[1]) and (pos[1][0] == sp2[0] + 2) and (pos[1][1] == sp2[1]):     # push 2 by 2 up
                    changed_board.grid[sp1[0] + 2][sp1[1]] = '.'
                    changed_board.grid[sp2[0] + 2][sp2[1]] = '.'
                    changed_board.grid[sp1[0] + 1][sp1[1]] = char_goal
                    changed_board.grid[sp2[0] + 1][sp2[1]] = char_goal
                    changed_board.grid[sp1[0]][sp1[1]] = char_goal
                    changed_board.grid[sp2[0]][sp2[1]] = char_goal
                    return changed_board
                elif (pos[0][0] == sp1[0]) and (pos[0][1] == sp1[1] - 2) and (pos[1][0] == sp2[0]) and (pos[1][1] == sp2[1] - 2):     # push 2 by 2 to the left 
                    changed_board.grid[sp1[0]][sp1[1] - 2] = '.'
                    changed_board.grid[sp2[0]][sp2[1] - 2] = '.'
                    changed_board.grid[sp1[0]][sp1[1] - 1] = char_goal
                    changed_board.grid[sp2[0]][sp2[1] - 1] = char_goal
                    changed_board.grid[sp1[0]][sp1[1]] = char_goal
                    changed_board.grid[sp2[0]][sp2[1]] = char_goal
                    return changed_board
                elif (pos[0][0] == sp1[0]) and (pos[0][1] == sp1[1] + 2) and (pos[1][0] == sp2[0]) and (pos[1][1] == sp2[1] + 2):     # push 2 by 2 to the right 
                    changed_board.grid[sp1[0]][sp1[1] + 2] = '.'
                    changed_board.grid[sp2[0]][sp2[1] + 2] = '.'
                    changed_board.grid[sp1[0]][sp1[1] + 1] = char_goal
                    changed_board.grid[sp2[0]][sp2[1] + 1] = char_goal
                    changed_board.grid[sp1[0]][sp1[1]] = char_goal
                    changed_board.grid[sp2[0]][sp2[1]] = char_goal
                    return changed_board
            elif p_mov == '<>':
                if (pos[0][0] == sp1[0]) and (pos[0][1] == sp1[1] - 2) and (pos[1][0] == sp2[0]) and (pos[1][1] == sp2[1] - 2):     # push 2 by 1 right by 2 spaces
                    #print('355')
                    '''changed_board.display()
                    input()
                    board.display()
                    input()'''
                    changed_board.grid[sp1[0]][sp1[1] - 2] = '.'
                    changed_board.grid[sp2[0]][sp2[1] - 2] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '<'
                    changed_board.grid[sp2[0]][sp2[1]] = '>'
                    return changed_board
                elif (pos[0][0] == sp1[0]) and (pos[0][1] == sp1[1] + 2) and (pos[1][0] == sp2[0]) and (pos[1][1] == sp2[1] + 2):    # push 2 by 1 left by 2 spaces                 
                    #print('363')
                    changed_board.grid[sp1[0]][sp1[1] + 2] = '.'
                    changed_board.grid[sp2[0]][sp2[1] + 2] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '<'
                    changed_board.grid[sp2[0]][sp2[1]] = '>'
                    return changed_board
                elif (pos[0][0] == sp1[0] + 1) and (pos[0][1] == sp1[1]) and (pos[1][0] == sp2[0] + 1) and (pos[1][1] == sp2[1]):     # push 2 by 1 up by 1 space
                    #print('371')
                    changed_board.grid[sp1[0] + 1][sp1[1]] = '.'
                    changed_board.grid[sp2[0] + 1][sp2[1]] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '<'
                    changed_board.grid[sp2[0]][sp2[1]] = '>'
                    return changed_board
                elif (pos[0][0] == sp1[0] - 1) and (pos[0][1] == sp1[1]) and (pos[1][0] == sp2[0] - 1) and (pos[1][1] == sp2[1]):     # push 2 by 1 down by 1 space
                    #print('379')
                    changed_board.grid[sp1[0] - 1][sp1[1]] = '.'
                    changed_board.grid[sp2[0] - 1][sp2[1]] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '<'
                    changed_board.grid[sp2[0]][sp2[1]] = '>'
                    return changed_board
            elif p_mov == '^v':
                #print(move, move[-2], sp1)
                if (pos[0][0] == sp1[0]) and (pos[0][1] == sp1[1] - 1) and (pos[1][0] == sp2[0]) and (pos[1][1] == sp2[1] - 1):     # push 1 by 2 right by 1 space
                    #print("394")
                    changed_board.grid[sp1[0]][sp1[1] - 1] = '.'
                    changed_board.grid[sp2[0]][sp2[1] - 1] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '^'
                    changed_board.grid[sp2[0]][sp2[1]] = 'v'
                    return changed_board
                elif (pos[0][0] == sp1[0]) and (pos[0][1] == sp1[1] + 1) and (pos[1][0] == sp2[0]) and (pos[1][1] == sp2[1] + 1):    # push 1 by 2 left by 1 space
                    changed_board.grid[sp1[0]][sp1[1] + 1] = '.'
                    changed_board.grid[sp2[0]][sp2[1] + 1] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '^'
                    changed_board.grid[sp2[0]][sp2[1]] = 'v'
                    return changed_board
                elif (pos[0][0] == sp1[0] + 2) and (pos[0][1] == sp1[1]) and (pos[1][0] == sp2[0] + 2) and (pos[1][1] == sp2[1]):     # push 1 by 2 up by 2 spaces
                    changed_board.grid[sp1[0] + 2][sp1[1]] = '.'
                    changed_board.grid[sp2[0] + 2][sp2[1]] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '^'
                    changed_board.grid[sp2[0]][sp2[1]] = 'v'
                    return changed_board
                elif (pos[0][0] == sp1[0] - 2) and (pos[0][1] == sp1[1]) and (pos[1][0] == sp2[0] - 2) and (pos[1][1] == sp2[1]):     # push 1 by 2 up by 2 spaces
                    changed_board.grid[sp1[0] - 2][sp1[1]] = '.'
                    changed_board.grid[sp2[0] - 2][sp2[1]] = '.'
                    changed_board.grid[sp1[0]][sp1[1]] = '^'
                    changed_board.grid[sp2[0]][sp2[1]] = 'v'
                    return changed_board
            
    else:   # spaces
        sp = move[-2][0]
        pos = move[-5]
        p_mov = move[-4]
        if len(move[-5]) > 1:   # num of piece's grid spots
            if p_mov == '^v':
                if (pos[0][0] == sp[0] - 1) and (pos[0][1] == sp[1]) and (pos[1][0] == sp[0] - 2) and (pos[1][1] == sp[1]):     # push 1 by 2 piece down by 1 space
                    # ^
                    # v is above
                    # -
                    changed_board.grid[sp[0] - 2][sp[1]] = '.'
                    changed_board.grid[sp[0] - 1][sp[1]] = '^'
                    changed_board.grid[sp[0]][sp[1]] = 'v'
                    return changed_board
                elif (pos[0][0] == sp[0] + 1) and (pos[0][1] == sp[1]) and (pos[1][0] == sp[0] + 2) and (pos[1][1] == sp[1]):     # push 1 by 2 piece up by 1 space
                    # -
                    # ^
                    # v is below
                    changed_board.grid[sp[0] + 2][sp[1]] = '.'
                    changed_board.grid[sp[0] + 1][sp[1]] = 'v'
                    changed_board.grid[sp[0]][sp[1]] = '^'
                    return changed_board
            elif p_mov == '<>':
                if (pos[0][0] == sp[0]) and (pos[0][1] == sp[1] - 1) and (pos[1][0] == sp[0]) and (pos[1][1] == sp[1] - 2):     # push 2 by 1 piece right by 1 space
                    # <>- on the left
                    #print('438')
                    changed_board.grid[sp[0]][sp[1] - 2] = '.'
                    changed_board.grid[sp[0]][sp[1] - 1] = '<'
                    changed_board.grid[sp[0]][sp[1]] = '>'
                    return changed_board
                elif (pos[0][0] == sp[0]) and (pos[0][1] == sp[1] + 1) and (pos[1][0] == sp[0]) and (pos[1][1] == sp[1]  + 2):     # push 2 by 1 piece left by 1 space
                    # -<> is on the right
                    #print('447')
                    changed_board.grid[sp[0]][sp[1] + 2] = '.'
                    changed_board.grid[sp[0]][sp[1] + 1] = '>'
                    changed_board.grid[sp[0]][sp[1]] = '<'
                    return changed_board
        else:
            if p_mov == char_single:
                if (pos[0][0] == sp[0] - 1) and (pos[0][1] == sp[1]):
                    changed_board.grid[sp[0] - 1][sp[1]] = '.'
                    changed_board.grid[sp[0]][sp[1]] = char_single
                    #changed_board.display()
                    return changed_board
                elif (pos[0][0] == sp[0] + 1) and (pos[0][1] == sp[1]):
                    changed_board.grid[sp[0] + 1][sp[1]] = '.'
                    changed_board.grid[sp[0]][sp[1]] = char_single
                    #changed_board.display()
                    return changed_board
                elif (pos[0][0] == sp[0]) and (pos[0][1] == sp[1] - 1):
                    changed_board.grid[sp[0]][sp[1] - 1] = '.'
                    changed_board.grid[sp[0]][sp[1]] = char_single
                    #changed_board.display()
                    return changed_board
                elif (pos[0][0] == sp[0]) and (pos[0][1] == sp[1] + 1):
                    changed_board.grid[sp[0]][sp[1] + 1] = '.'
                    changed_board.grid[sp[0]][sp[1]] = char_single
                    #changed_board.display()
                    return changed_board
    '''x = input()
    changed_board.display()'''
    #print('\n')
    
    return changed_board

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, f, depth, space, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = get_f(board, depth)
        self.depth = depth
        self.parent = parent
        self.id = hash(board)  # The id for breaking ties.
        # added this in
        self.space = space

    # print out the attributes of a piece for debugging
    def __str__(self):
        print('\n')
        self.board.display() 
        #self.board.grid
        return f'\nNew: f: {self.f}, depth: {self.depth}, parent: {self.parent}, id: {self.id}, space: {self.space}'
    
    def __lt__(self, other):
        if other.f > self.f:
            return other
        return self
    
    


class Moves:
    def __init__(self, State, count):
        self.moves = count
        self.state =  State

# Returns a list of successor state            
def gen_states(parent, pieces):
    main_board = parent.board
    out = []  # list of successor states
    # find all the legal moves that could be played with parent's board configuration
    #input()
    #print("NEW board")
    #main_board.display()
    all_moves = main_board.legality()
    #print(all_moves)
    # create a new state object with the resulting board of each legal move
    for move in all_moves:
        space = move[-3]   # find number of spaces moved
        # using the o.g. board to enact changes on a new board
        changed_board = Board(pieces)
        changed_board = change_board(move, changed_board, main_board)
        node = State(changed_board, parent.f, parent.depth + 1, parent.space + space, parent)    
        #print("move", move)
        #node.board.display()
        out.append(node)
    out.reverse()
    # return a list of all the states
    return out

# Return seq of states until the initial state reference
def get_sol(state):
    par_l = [state]
    # add next parent
    par = state.parent
    while par.parent != None:
        par = State(par.board, par.f, par.depth, par.parent)
        par_l.append(par)
    par_l.reverse()
    
    for p in par_l:
        p.board.display()

    return par_l  # initial state to the goal state


# function that takes a state and returns the state's heuristic value
# implement Manhattan Distance: sum of the Manhattan distances of the tiles to their goal positions
def get_f(board, depth):
    goal = []
    # find the goal pieces
    col = 0
    for i, line in enumerate(board.grid):
        for ch in line:
            if ch == '1':
                goal.append((i, col))
            col += 1
        col = 0
    
    # reff: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html  
    x = abs(max(goal[0][0], goal[1][0], goal[2][0], goal[3][0]) - 4)
    y = abs(max(goal[0][1], goal[1][1], goal[2][1], goal[3][1]) - 2)
    h = x + y
    f = h + depth + 1

    '''x = abs(goal[0][0] - 4)
    y = abs(goal[0][1] - 2)
    h = x + y
    f = h + (depth + 1)'''

    return f

def clear_heap(front):
    while len(front) > 0:
        front.pop()

    return front

'''def DFS(init_state, pieces):
    # start with generic search algo
    Frontier = [(init_state.f, init_state.id, init_state.board.grid, init_state)]
    heapify(Frontier)
    Explored = []
    soln_states = []
    while len(Frontier) > 0:
        curr_f, curr_id, curr_grid, curr = heappop(Frontier)
        if (curr_grid in Explored) == False:
            # this parent grid has been explored
            Explored.append(curr_grid) 
            if curr.board.goal_test():
                #return get_sol(curr)
                return curr
            for s in gen_states(curr, pieces):
                # main comparator is # space with id as a tie breaker
                heappush(Frontier, (s.f, s.id, s.board.grid, s))
              
   
    return None'''

def DFS(init_state, pieces):
    Frontier=[init_state]
    #Explored = set()
    Explored=[]
    while len(Frontier) > 0:
        curr = Frontier.pop()
        #curr.board.display()
        #input()
        #print("this is ")
        #print(Explored)
        explored=False
        for e in Explored:
            if e.board.grid == curr.board.grid:
                explored=True
                break
        #input()
        if not explored:
        #if curr not in Explored:
            #Explored.add(curr)
            Explored.append(curr)
            if curr.board.goal_test():
                return curr
            new_states = gen_states(curr, pieces)
            for s in new_states:
                #s.board.display()
                #input()
                Frontier.append(s)    
    return None
        


def read_from_file(filename1, filename2):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename1, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):

            if ch == '^': # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<': # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if g_found == False:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)

    # initial state and returns the first solution found by DFS
    parent = State(board, 0, 0, 0)
    sol = DFS(parent, pieces)

    states = []
    curr_state = sol
    while curr_state.parent != None:
        states.append(curr_state)
        curr_state = curr_state.parent
    states.append(parent)
    states.reverse()

    '''for s in states:
        s.board.display()
        print('\n')'''
    #parent.board.display()
    #print(sol)
    
    ''' sol_file = open(filename2, "w")
    if sol == None:
        ch = "None"
        sol_file.write(ch)
    else:
        for s in sol:
            for i, line in enumerate(s.board.grid):
                for ch in line:
                    if ch != None:
                        sol_file.write(ch)
                sol_file.write('\n')
            sol_file.write('\n')'''
    
    sol_file = open(filename2, "w")
    if sol == None:
        ch = "None"
        sol_file.write(ch)
    else:
        #sol.display()
        for sol in states:
            grid = sol.board 
            for line in grid.grid:
                for peice in line:
                    sol_file.write(peice)
                sol_file.write('\n')
            sol_file.write('\n')

    return board


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board = read_from_file(args.inputfile, args.outputfile)
    


# test it on more inputs
# successor function @Intput: board , @Output: list of board 
# legal_moves,  for each move in legal_moves : apply(board,move): @Output: Board
# a list of boards -> will be the successor or in dfs terms neighbours of the board (@Intput)


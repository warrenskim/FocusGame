# Author: Warren Kim
# Date: December 3, 2020
# Description: This file simulates the FOCUS game, which can be played between two people.
#               Instructions and info: https://en.wikipedia.org/wiki/Focus_%28board_game%29

class FocusGame:
    """
    This class creates the FocusGame object, which can be used to play Focus.
    The Board class will initiate separately, but please note that the coordinate (0,0) refers
    to the top left corner of the board, with the first value referring to the ROW and the second
    value referring to the COLUMN. Therefore, coordinates are given in (Y,X) form.
    """

    def __init__(self, infoA, infoB):
        """
        This method will be initiated by setting up values corresponding to each
        player's information. It also initializes the Board class and creates the
        self._turn variable, which will be changed upon the first move.
        :param infoA: Tuple containing 1. Player A's name and 2. Player A's color
        :param infoB: Tuple containing 1. Player B's name and 2. Player B's color
        """
        self._infoA = infoA
        self._infoB = infoB
        self._turn = None
        self._offTurn = None
        self._board = Board(infoA, infoB)

    def move_piece(self, playerName, orig, dest, piecesMoved):
        """
        This method works by first checking if the move entered is a valid one.
        If not, it will display the corresponding error message. If the move is valid,
        self._turn will switch to the other player, and our Board class will make the move.
        :param playerName: Player making the move
        :param orig: Tuple containing origin coordinates in (y,x) form
        :param dest: Tuple containing destination coordinates in (y,x) form
        :param piecesMoved: Number of pieces to be moved from top of origin stack
        :return: Message indicating the effects of the command
        """
        # Setting up self._turn if it is the first move:
        if self._turn is None:
            if playerName == self._infoA[0]:
                self._turn = self._infoA
                self._offTurn = self._infoB
            elif playerName == self._infoB[0]:
                self._turn = self._infoB
                self._offTurn = self._infoA

        # To ensure the correct player is making the move:
        if self._turn[0] != playerName:
            return "Not your turn"

        # To ensure that our origin and destination are on the board. We can
        #   customize the messages for invalid origin/destination, if desired:
        elif orig[0] < 0 or orig[0] > 5 or orig[1] < 0 or orig[1] > 5:
            return "Invalid location"
        elif dest[0] < 0 or dest[0] > 5 or dest[1] < 0 or dest[1] > 5:
            return "Invalid location"

        # To ensure that we are moving the correct number of spaces
        #   AND to ensure that we are not moving diagonally:
        elif abs(orig[0] - dest[0]) + abs(orig[1] - dest[1]) != piecesMoved:
            return "Invalid number of spaces"

        # To ensure that the number of pieces moved is within the origin stack size range:
        elif piecesMoved > len(self._board.show_pieces(orig)):
            return "Invalid number of pieces"

        # To ensure that the origin stack CAN be moved by the player, we will check to see
        #   if the top piece matches the current turn color:
        elif self.show_pieces(orig)[-1] != self._turn[1]:
            return "Invalid selection -- not your color"

        # If valid, switch the turns and let the board make the move for us:
        else:
            placeholder = self._turn
            self._turn = self._offTurn
            self._offTurn = placeholder
            return self._board.move_piece(playerName, orig, dest, piecesMoved)

    def show_pieces(self, pos):
        """
        This method will take the coordinates of the position and plug them into the
        Board class. This will then access the list at that particular coordinate, which
        will consist of the current game pieces at that coordinate.
        :param pos: A tuple containing the coordinates of the position in question (y,x)
        :return: List indicating which pieces are currently at the specified position
        """
        return self._board.show_pieces(pos)

    def show_reserve(self, playerName):
        """
        This method will access the variable which corresponds to the player in question's
        reserve via the Board class. That value will be returned for the user.
        :param playerName: Name of the player in question
        :return: Pieces in the player's reserve
        """
        return self._board.show_reserve(playerName)

    def show_captured(self, playerName):
        """
        This method will access the variable which corresponds to the player in question's
        captured pile via the Board class. That value will be returned for the user.
        :param playerName: Name of the player in question
        :return: Pieces that the player captured from opponent
        """
        return self._board.show_captured(playerName)

    def reserved_move(self, playerName, dest):
        """
        This method first checks if the player has pieces in their reserve. If they do,
        we change self._turn to the other player and pass the move along to our Board class
        :param playerName: The player who is making the move
        :param dest: Tuple containing coordinates (y,x) in which to place reserved piece
        :return: Message regarding the status of the move
        """
        reserve = self.show_reserve(playerName)
        if reserve == 0:
            return "No pieces in reserve"
        # Switching turns
        placeholder = self._turn
        self._turn = self._offTurn
        self._offTurn = placeholder
        # Making our move via Board:
        return self._board.reserved_move(playerName, dest)


class Board:
    """
    This class creates and manages the board that the players play on. It can be used
    to move pieces around and see what's on the board. It also manages the reserve and
    captured piles for both players.
    """

    def __init__(self, infoA, infoB):
        """
        FOCUS board is initialized as a list of 6 lists, each corresponding to a row.
        Each row holds 6 other lists, each corresponding a column.

        PLEASE NOTE: the coordinate (0,0) refers to the top left corner of the board, with
        the first value referring to the ROW and the second value referring to the COLUMN.
        Therefore, coordinates are given in (y,x) form.

        :param infoA: Tuple containing 1. Player A's name and 2. Player A's color
        :param infoB: Tuple containing 1. Player B's name and 2. Player B's color
        """
        self._infoA = infoA
        self._reserveA = 0
        self._capturedA = 0
        self._infoB = infoB
        self._reserveB = 0
        self._capturedB = 0

        self._row0 = [['R'], ['R'], ['G'], ['G'], ['R'], ['R']]
        self._row1 = [['G'], ['G'], ['R'], ['R'], ['G'], ['G']]
        self._row2 = [['R'], ['R'], ['G'], ['G'], ['R'], ['R']]
        self._row3 = [['G'], ['G'], ['R'], ['R'], ['G'], ['G']]
        self._row4 = [['R'], ['R'], ['G'], ['G'], ['R'], ['R']]
        self._row5 = [['G'], ['G'], ['R'], ['R'], ['G'], ['G']]
        self._board = [self._row0, self._row1, self._row2, self._row3, self._row4, self._row5]
        # Board[y] will refer to row y (moving down)
        # Board[y][x] will refer to column x (moving right) in row y (moving down)

    def move_piece(self, playerName, orig, dest, piecesMoved):
        """
        This method will move the pieces for our Focus game. The FocusGame class ensures that
        the move is a valid one. Only then will the method be passed to Board.
        :param playerName: The player making the move
        :param orig: Tuple containing the coordinates (y,x) of the stack we want to move
        :param dest: Tuple containing the coordinates (y,x) of the stack destination
        :param piecesMoved: The number of pieces we want to move
        :return: Message corresponding to the move (successful move vs player win)
        """
        # Move the last *piecesMoved* number of pieces from orig to a new list (moving = [])
        moving = []aaaaaaaaa
        y = orig[0]
        x = orig[1]
        for number in range (0,piecesMoved):
            moving.append(self._board[y][x][-1])
            del self._board[y][x][-1]

        # Move all of those values to the end of dest, while simultaneously clearing moving list
        #   Notice we are re-setting x and y to our destination coordinates
        y = dest[0]
        x = dest[1]
        while moving:
            self._board[y][x].append(moving[-1])
            del moving[-1]

        # Check if dest is > 5. If so, move excess pieces to moving, since it is now empty
        length = len(self._board[y][x])
        if length > 5:
            excess = length - 5
            for number in range(0,excess):
                moving.append(self._board[y][x][0])
                del (self._board[y][x][0])

        # Here, use the if playerName section to add the correct colors to reserve/captured:
        if playerName == self._infoA[0]:
            while moving:
                if moving[0] == self._infoA[1]:
                    self._reserveA += 1
                else:
                    self._capturedA += 1
                del moving[0]
        elif playerName == self._infoB[0]:
            while moving:
                if moving[0] == self._infoB[1]:
                    self._reserveB += 1
                else:
                    self._capturedB += 1
                del moving[0]

        # Finally, check if either play won. If not, return the "successfully moved" message
        if self._capturedA >= 6:
            return self._infoA[0] + " Wins!"
        elif self._capturedB >= 6:
            return self._infoB[0] + " Wins!"
        else:
            return "Successfully moved"

    def show_pieces(self, pos):
        """
        This returns the values (a list) at the coordinates given.
        :param pos: Tuple containing the coordinates in question (y,x)
        :return: The list contained at that coordinate.
        """
        y = pos[0]
        x = pos[1]
        pieces = self._board[y][x]
        return pieces

    def show_reserve(self, playerName):
        """
        This method will access the variable which responds to the player in question's
        reserve. That variable will be returned for the user.
        :param playerName: Name of the player in question
        :return: Pieces in the player's reserve
        """
        if playerName == self._infoA[0]:
            return self._reserveA
        elif playerName == self._infoB[0]:
            return self._reserveB
        else:
            return "Invalid input"

    def show_captured(self, playerName):
        """
        This method will access the variable which corresponds to the player in question's
        capture pile. That variable will be returned for the user.
        :param playerName: Name of the player in question
        :return: Pieces that the player captured from opponent
        """
        if playerName == self._infoA[0]:
            return self._capturedA
        elif playerName == self._infoB[0]:
            return self._capturedB
        else:
            return "Invalid input"

    def reserved_move(self, playerName, dest):
        """
        This method will place a piece (from the player's reserve) onto the destination
        location coordinates (y,x). The FocusGame class ensures that the move being made
        is a valid one, then passes it along to the Board class.
        :param playerName: The player making the reserved move
        :param dest: Tuple containing coordinates (y,x) for the reserved piece
        :return: Successful message, since the move has been approved by FocusGame class
        """
        y = dest[0]
        x = dest[1]
        # Add the correct color to destination, then subtract 1 from reserve:
        if playerName == self._infoA[0]:
            color = self._infoA[1]
            self._board[y][x].append(color)
            self._reserveA -= 1
        elif playerName == self._infoB[0]:
            color = self._infoB[1]
            self._board[y][x].append(color)
        # Check if list is > 5. If so, delete the first item in the list:
        if len(self._board[y][x]) > 5:
            del self._board[y][x][0]
        # Return successful message:
        return "Successfully moved"

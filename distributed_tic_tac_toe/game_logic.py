"""
Thi module contains the logic for the game.

The game is played on a 3x3 board. The board is represented by a list of lists.
Each inner list represents a row on the board. Each element in the inner list
represents a cell on the board. The value of the element is either 'X', 'O', or
None. The value of the element is None if the cell is empty.

The game is played by two players. The players take turns placing their
respective marks on the board. The first player to get 3 marks in a row (up,
down, across, or diagonally) is the winner. If all 9 cells are filled and no
player has 3 marks in a row, then the game is a tie.

The game is played by calling the start-game function. The start-game function
takes a list of two players as its only argument. 
"""


class Board:
    """A class that represents the game board."""

    def __init__(self):
        """Initialize the board."""
        self.board = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]

    def __str__(self):
        """Return a string representation of the board."""
        return str(self.board)

    def is_full(self):
        """Return True if the board is full."""
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def is_empty(self):
        """Return True if the board is empty."""
        for row in self.board:
            for cell in row:
                if cell is not None:
                    return False
        return True

    def get_board(self):
        """Return the board."""
        return self.board

    def is_valid_move(self, row, column):
        """Return True if the move is valid."""
        if row < 0 or row > 2:
            return False
        if column < 0 or column > 2:
            return False
        if self.board[row][column] is not None:
            return False
        return True

    def set_symbol(self, coordinate, symbol):
        """
        This command is used by a player during its turn to fill the board with its assigned symbol.  
        Each cell position in the board is assigned with a unique identifier. 
        From top to bottom and left to right. (1,2,3;4,5,6;7,8,9). 
        """
        row = (coordinate - 1) // 3
        column = (coordinate - 1) % 3
        self.board[row][column] = symbol

    def get_winner(self):
        """Return the winner of the game."""
        # Check the rows.
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]
        # Check the columns.
        for column in range(3):
            if self.board[0][column] == self.board[1][column] == \
                    self.board[2][column] and self.board[0][column] is not None:
                return self.board[0][column]
        # Check the diagonals.
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and \
                self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and \
                self.board[0][2] is not None:
            return self.board[0][2]
        # If we get here, then there is no winner.
        return None

    def list_board(self):
        """Return a list of the board."""
        board_list = []
        for row in self.board:
            for cell in row:
                board_list.append(cell)
        return board_list


def start_game(players):
    """Start the game."""
    # Print the board.
    print_board()
    # Get the first player.
    player = players[0]
    # Loop until the game is over.
    while True:
        # Get the move from the player.
        move = player.get_move(board)
        # Check if the move is valid.
        if board.is_valid_move(move):
            # Set the move on the board.
            board.set_move(move, player.get_symbol())
            # Print the board.
            print_board()
            # Check if the game is over.
            if board.is_full() or board.get_winner() is not None:
                # Print the winner.
                print_winner()
                # Exit the game loop.
                break
            # Switch players.
            player = switch_player(player, players)
        else:
            # Print an error message.
            print('Invalid move. Try again.')


def print_board():
    """Print the board."""
    print(board)


def print_winner():
    """Print the winner."""
    winner = board.get_winner()
    if winner is not None:
        print(winner, 'wins!')
    else:
        print('Tie game.')


def switch_player(player, players):
    """Switch players."""
    if player == players[0]:
        return players[1]
    else:
        return players[0]


class Player:
    """A class that represents a player."""

    def __init__(self, symbol):
        """Initialize the player."""
        self.symbol = symbol

    def get_symbol(self):
        """Return the player's symbol."""
        return self.symbol

    def get_move(self, board):
        """Get the player's move."""
        while True:
            try:
                move = int(input('Enter a move: '))
                if board.is_valid_move(move):
                    return move
                else:
                    print('Invalid move. Try again.')
            except ValueError:
                print('Invalid move. Try again.')


# play
# instantiate the board
board = Board()

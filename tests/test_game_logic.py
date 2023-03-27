"""
test the game_logic module.
"""
import random
from distributed_tic_tac_toe.game_logic import Board


# Test the Board class.
def test_board():
    """
    test if the board is full.
    """
    board = Board()
    # fill the board with random values
    for row in range(3):
        for column in range(3):
            board.board[row][column] = random.choice(['X', 'O'])
    # test the is_full method
    assert board.is_full() is True


def test_board_is_empty():
    """
    test if the board is empty.
    """

    board = Board()
    assert board.is_empty() is True


def test_set_symbol():
    """
    test if the set_symbol method works.
    """
    board = Board()
    board.set_symbol(1, 'X')
    board.set_symbol(1, 'X')
    board.set_symbol(2, 'O')
    board.set_symbol(7, 'X')
    assert board.board[0][0] == 'X'
    assert board.board[0][0] == 'X'
    assert board.board[0][1] == 'O'
    assert board.board[2][0] == 'X'


def test_get_winer():
    """
    test if the get_winner method works.
    """
    board = Board()
    board.set_symbol(1, 'X')
    board.set_symbol(2, 'X')
    board.set_symbol(3, 'X')
    assert board.get_winner() == 'X'

    board = Board()
    board.set_symbol(4, 'O')
    board.set_symbol(5, 'O')
    board.set_symbol(6, 'O')
    assert board.get_winner() == 'O'

    board = Board()
    board.set_symbol(1, 'X')
    board.set_symbol(4, 'X')
    board.set_symbol(7, 'X')
    assert board.get_winner() == 'X'

    board = Board()
    board.set_symbol(2, 'O')
    board.set_symbol(5, 'O')
    board.set_symbol(8, 'O')
    assert board.get_winner() == 'O'

    board = Board()
    board.set_symbol(1, 'X')
    board.set_symbol(5, 'X')
    board.set_symbol(9, 'X')
    assert board.get_winner() == 'X'

    board = Board()
    board.set_symbol(3, 'O')
    board.set_symbol(5, 'O')
    board.set_symbol(7, 'O')
    assert board.get_winner() == 'O'

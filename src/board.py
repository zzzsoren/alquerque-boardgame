from move import *
from functools import reduce

# the board is represented as a list of strings with the first position (index 0) being the player turn.
# position (index) 1-25 in the string correnspond to a position on the board.
Board = list[str]
SIZE = 5
WHITE, BLACK, EMPTY = "w", "b", " "

def _coord(pos: int) -> tuple[int, int]:
    """Converts a board position to coordinates (x, y).
    >>> _coord(1)
    (0, 0)
    >>> _coord(24)
    (3, 4)
    """
    x = (pos - 1) % SIZE
    y = (pos - 1) // SIZE
    return x, y

def make_board() -> Board:
    """Initializes a 5x5 board with 
    Position 0: is the current player turn (white starts), 1 - 12 is black pieces, 14 - 25 is white pieces
    >>> make_board()
    ['w', 
    'b', 'b', 'b', 'b', 'b',
    'b', 'b', 'b', 'b', 'b',
    'b', 'b', ' ', 'w', 'w',
    'w', 'w', 'w', 'w', 'w',
    'w', 'w', 'w', 'w', 'w']
    """
    return ["w"] + ["b" for x in range(12)] + [" "] +  ['w' for x in range(12)]

def white_plays(b: Board) -> bool:
    """Determines whether it's the white players turn.
    >>> white_plays(['w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'])
    True
    >>> white_plays(['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'])
    False
    """
    return b[0] == "w"

def is_legal(m: Move, b: Board) -> bool:
    """Determines whether a move is legal on the current board.
    >>> b = make_board()
    >>> is_legal((17, 13), b)
    True
    >>> is_legal((16, 13), b)
    False
    """
    return (b[0] == b[source(m)] and b[target(m)] == EMPTY and 
        ((source(m)%2 != 0 and _legal_odd(m, b)) or 
         (source(m)%2 == 0 and _legal_even(m, b)) or 
         _capture(m, b)))

def _legal_even(m: Move, b: Board) -> bool:
    """Determines whether a move is legal on an even position on the current board.
    >>> b = make_board()
    >>> _legal_even((18,13), b)
    True
    >>> _legal_even((16,13), b)
    False
    """
    sx, sy = _coord(source(m))
    tx, ty = _coord(target(m))
    # W rykker en op eller B rykker 1 ned
    return (abs(sx - tx) == 0 and 
            ((b[0] == WHITE and ty - sy == -1) or 
             (b[0] == BLACK and ty - sy == 1)))

def _legal_odd(m: Move, b: Board) -> bool:
    """"Determines whether a move is legal on an odd position on the current board.
    >>> b = make_board()
    >>> _legal_odd((17,13), b)
    True
    >>> _legal_odd((23,13), b)
    False 
    """
    sx, sy = _coord(source(m))
    tx, ty = _coord(target(m))
    # 1 sidelens højst
    # W rykker 1 op eller B rykker 1 ned
    return (abs(sx - tx) <= 1 and 
            ((b[0] == WHITE and ty - sy == -1) or
             (b[0] == BLACK and ty - sy == 1)))

def _capture(m: Move, b: Board):
    """Determines whether a move is a valid capture on the current board.
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', 'w', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    >>> _capture((8, 18), b)
    True
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', 'w', ' ', 'w', ' ', 'w', 'w', 'w', 'w', 'w']
    >>> _capture((18, 20), b)
    True
    ['w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', 'w', ' ', 'b', ' ', 'w', 'w', 'w', 'w', 'w']
    >>> _capture((25, 13), b)
    True
    """
    sx, sy = _coord(source(m))
    tx, ty = _coord(target(m))
    # 2 op/ned
    # 2 sidelens
    # 2op/ned og 2sidelens
    # Mellempositionen ejet at modstander
    return ((abs(tx - sx) == 0 and abs(ty - sy) == 2 or 
             abs(tx - sx) == 2 and abs(ty - sy) == 0 or 
             source(m)%2 != 0 and abs(tx - sx) == 2 and abs(ty - sy) == 2) and
            b[(source(m) + target(m))//2] == _enemy(b))

def _is_capture(m: Move) -> bool:
    """Determines whether a move is a capture on the current board.
    >>> _is_capture((25, 15))
    True
    >>> _is_capture((25, 13))
    True
    >>> _is_capture((25, 19))
    False
    >>> _is_capture((25, 20))
    False
    """
    sx, sy = _coord(source(m))
    tx, ty = _coord(target(m))
    return abs(ty - sy) > 1 or abs(tx - sx) > 1

def _enemy(b: Board) -> str:
    """Returns the players enemy."""
    return "b" if b[0] == "w" else "w"

def legal_moves(b: Board) -> list[Move]:
    """Finds all legal moves for the current player on the current board.
    >>> b = make_board()
    >>> legal_moves(b)
    [(17, 13), (18, 13), (19, 13)]
    """
    positions = white(b) if white_plays(b) else black(b)
    return [(p, t) for p in positions for t in range(1, 26) if is_legal((p, t), b)]

def white(b: Board) -> list[int]:
    """Returns the positions of the white pieces on the board.
    ['w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', 'w', ' ', 'b', ' ', 'w', 'w', 'w', 'w', 'w']
    >>> white(b)
    [0, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25]
    """
    return [i for i, x in enumerate(b) if x == "w" and i != 0]

def black(b: Board) -> list[int]:
    """Returns the positions of the black pieces on the board.
    ['w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', 'w', ' ', 'b', ' ', 'w', 'w', 'w', 'w', 'w']
    >>> black(b)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19]
    """
    return [i for i, x in enumerate(b) if x == "b" and i != 0]

def move(m: Move, b: Board) -> None:
    """Simulates the move on the board
    ['w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    >>> move((18, 13), b)
    >>> b
    ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'w', 'w', 'w', 'w', 'w', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w']

    """
    b[source(m)] = EMPTY
    b[target(m)] = b[0]
    if _is_capture(m):
        b[(source(m) + target(m))//2] = EMPTY
    b[0] = _enemy(b)

def is_game_over(b: Board) -> bool:
    """Determines whether the game is over"""
    return legal_moves(b) == []

def copy(b: Board) -> Board:
    """Copies the board
    >>> b = make_board()
    >>> copy_board(b)
    ['w', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    """
    return [x for x in b]

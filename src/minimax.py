from board import Board, legal_moves
from move import Move
from Tree import *

def next_move(b: Board, n: int = 3) -> Move:
    """Returns the next move for the autoplayer."""
    tree = make_tree(b, n)
    # Blad noder er min node
    if n % 2 == 0:
        best = find_min(tree)
    else:
        best = find_max(tree)

    return get_move(best)

def get_move(leaf: Node) -> Move:
    if leaf.previous_node.from_move == (0, 0):
        return leaf.from_move
    else:
        return get_move(leaf.previous_node)


from dataclasses import dataclass
from functools import reduce
from board import *

def next_move(b: Board, n: int = 3) -> Move:
    """Returns the next move for the autoplayer."""
    tree = make_tree(b, n)
    return _next_move(find_max(tree))

@dataclass
class Node:
    board: Board
    parent: None         # Node
    parent_move: Move
    moves: list[Move]
    child_nodes: list    # list[Node]
    maximizing: bool
    value: int

def make_node(board: Board,
              parent: Node=None,
              parent_move: Move=(0, 0), # har betydning for evalueringsfunktionen
              maximizing: bool=True,
              value: int=None) -> Node: 
    """Returns a node representing the state of the game."""
    return Node(board, parent, parent_move, node_moves(board), [], maximizing, value)

def node_moves(board: Board) -> list[Move]:
    """Returns the legal capturing moves if any otherwise returns the legal moves."""
    moves = legal_moves(board)
    captures = [m for m in moves if 6 < abs(m[0] - m[1]) or 3 > abs(m[0] - m[1])]
    return captures or moves

def expand_node(node: Node) -> None:
    """Adds possible state permutations to a state."""
    for m in node.moves:    
        new_board = copy(node.board)
        move(m, new_board)
        node.child_nodes.append(make_node(new_board, node, m, not node.maximizing))

def evaluate_node(node: Node) -> int:
    """Evaluates the how positive a state is based on the previous move (the enemy move)."""
    if node.child_nodes == []:
        # Evt win value
        return 0
    elif node.maximizing:
        # Fjendens captures er skidt for spilleren
        return 0 -_distance(node.parent_move)
    else:
        return  _distance(node.parent_move)

def _distance(move: Move) -> int:
    """Returns the absolute distance of a move."""
    return  abs(move[0] - move[1])

@dataclass
class Tree:
    root: Node
    leafes: list[Node]

def make_tree(board: Board,height: int) -> Tree:
    """Initializes a GameTree with a given height to a given board."""
    tree = Tree(make_node(board), [])
    construct_tree(tree.root, tree, height)
    return tree

def construct_tree(node: Node, tree: Tree, height: int, acc: int=-1)  -> None:
    """Builds the heuristic tree of a given height"""
    if height == 0 or node.moves == []:
        node.value = acc+evaluate_node(node)
        tree.leafes.append(node)
    else:
        expand_node(node)
        # Expand subnodes rekursivt
        for i in range(len(node.child_nodes)):
            construct_tree(node.child_nodes[i], tree, height-1, acc+evaluate_node(node.child_nodes[i]))

def find_max(tree) -> Node:
    """Returns the leaf with the maximum accumulated value"""
    return reduce(lambda x,y: x if x.value > y.value else y, tree.leafes)

def _next_move(leaf: Node) -> Move:
    if leaf.parent.parent_move == (0, 0):
        return leaf.parent_move
    else:
        return _next_move(leaf.parent)
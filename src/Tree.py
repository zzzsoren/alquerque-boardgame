from dataclasses import dataclass
from board import *
from functools import reduce

@dataclass
class Node:
    board: Board
    from_move: Move
    moves: list[Move]
    previous_node: None #Node
    next_nodes: list #list[Node]
    value: int
    maximizing: bool

def make_node(board: Board=make_board(), from_move: Move=(0, 0), prev: Node=None, max: bool=True, value: int=None) -> Node: 
    """Returns a node representing the state of the game."""
    return Node(board, from_move, moves(board), prev, [], value, max)

def moves(board: Board) -> list[Move]:
    """Returns the legal capturing moves if any otherwise returns the legal moves."""
    moves = legal_moves(board)
    return ([m for m in moves if 6 < abs(m[0] - m[1]) or 3 > abs(m[0] - m[1])] or moves)

def evaluate_node(node: Node) -> int:
    """Evaluates the how positive a state is based on the previous move"""
    if node.from_move[1] == 1 or node.from_move[1] == 5 or node.from_move[1] == 20 or node.from_move[1] == 25:
        bad_position = 3
    else:
        bad_position = 0

    # Fjendens captures er skidt for spilleren
    if node.maximizing and not node.next_nodes == []:
        return 0 - (abs(node.from_move[0] - node.from_move[1])) - bad_position
    elif not node.maximizing:
        return 0 + (abs(node.from_move[0] - node.from_move[1])) + bad_position
    else:
        return 0

def expand_node(node: Node) -> None:
    """Adds possible state permutations to a state"""
    for m in node.moves:    
        new_board = copy(node.board)
        move(m, new_board)
        node.next_nodes.append(make_node(new_board, m, node, not node.maximizing))


@dataclass
class Tree:
    root: Node
    height: int
    leafes: list[Node]

def make_tree(board: Board, height: int) -> Tree:
    """Initializes a GameTree with a given height to a given board."""
    tree = Tree(make_node(board), height, [])
    construct_tree(tree.root, height, tree.leafes)
    return tree

def construct_tree(node: Node, height: int, leafes:list[Node], acc: int=0)  -> None:
    """Builds the heuristic tree of a given height"""
    if height == 0 or node.moves == []:
        leafes.append(node)
        node.value = acc+evaluate_node(node)
    else:
        expand_node(node)
        # Expand subnodes rekursivt
        for i in range(len(node.next_nodes)):
            construct_tree(node.next_nodes[i], height-1, leafes, acc+evaluate_node(node.next_nodes[i]))

def find_max(tree) -> Node:
    """Returns the leaf with the maximum accumulated value"""
    best = tree.leafes[0]
    for leaf in tree.leafes:
        if leaf.value > best.value:
            best = leaf
    return best

def find_min(tree: Tree) -> Node:
    """Returns the leaf with the maximum accumulated value"""
    best = tree.leafes[0]
    for leaf in tree.leafes:
        if leaf.value < best.value:
            best = leaf
    return best

tree = make_tree(make_board(), 7)

#PRINT TRÆET
def print_tree(node: Node, depth: int=0):
    print("*"*(depth), "--"*depth, depth, "::", end="")
    print(node.board, node.from_move, node.previous_node == None)
    for sub_node in node.next_nodes:     
        print_tree(sub_node, depth+1)

print_tree(tree.root)
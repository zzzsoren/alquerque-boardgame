from dataclasses import dataclass
from board import *

def next_move(b: Board, n: int = 3) -> Move:
    """Returns the next move for the autoplayer."""
    tree = make_tree(b, n)
    best_value = minmax(tree.root.children[0], tree.root.is_white)
    best_path = tree.root.children[0]
    for i in range(tree.root.children):
        value = minmax(tree.root.children[i], tree.root.is_white)
        if  value > best_value:
            best_path = tree.root.children[i]
            best_value = value
    return best_path.prev_move

@dataclass
class Node:
    board: Board
    children: None #list[Node]
    prev_move: Move
    is_white: bool

@dataclass
class Tree:
    root: Node

def make_tree(board: Board, height: int) -> Tree:
    root = Node(board, [], None, white_plays(board))
    tree = Tree(root)
    expand(root)
    _make_tree(root, height)
    return tree

def _make_tree(node: Node, height: int):
    if height == 0 or node.children == []:
        return
    else:
        for child in node.children:
            expand(child)
            _make_tree(child, height - 1)

def expand(node: Node) -> list[Node]:
    for m in legal_moves(node.board):
        new = copy(node.board)
        move(m, new)
        node.children.append(Node(new, [], m, not node.is_white))

def minmax(node: Node, player_white: bool) -> int:
    if node.children == []:
        return evaluate(node)
    else:
        return (max([minmax(child, player_white) for child in node.children]) if node.is_white == player_white else 
                min([minmax(child, player_white) for child in node.children]))

def evaluate(node: Node) -> int:
    if node.is_white:
        return len(black(node.board)) - len(white(node.board))
    else:
        return len(white(node.board)) - len(black(node.board))

# For Printing treees
# def print_tree(node: Node, depth: int=0):
#     print("*"*(depth), "--"*depth, depth, "::", end="")
#     print(node.board, node.prev_move)
#     for child in list(node.children):     
#         print_tree(child, depth+1)
# tree = make_tree(make_board(), 7)
# print_tree(tree.root)



import board as b
import minimax

def print_menu() -> None:
    """Prints the select game mode menu in the console."""
    print("\t********** SELECT GAME MODE **********\n" +
          "\t|(1) PvP                              |\n" +
          "\t|(2) White vs CPU                     |\n" +
          "\t|(3) Black vs CPU                     |\n" +
          "\t|(4) CPU vs CPU                       |\n" +
          "\t|(0) Quit                             |\n" +
          "\t|      ~made by soren rosendahl~      |\n" +
          "\t**************************************")

def print_board(board: b.Board) -> None:
    """Prints the board in the console."""
    positions = _board_list(board)
    print("\t-----------       BLACK      ------------")
    for i in range(25):
        if i != 0 and i % 5 == 0:
            print("\t|\n" + 
                  "\t|\t|\t|\t|\t|\t|")
            print(f"\t|{i+1}:{positions[i]}", end="")
        else:
            print(f"\t|{i+1}:{positions[i]}", end="")
    print("\t|")
    print("\t-----------       WHITE      ------------")

def print_moves(board: b.Board) -> b.Move:
    """Prints the legal moves in the console."""
    print(f"\tDecisions:")
    moves = b.legal_moves(board)
    for i in range(len(moves)):
        if i != 0 and i % 3 == 0:
            print()
        move = moves[i]
        print(f"\t[{i+1}]: {move[0]} to {move[1]}", end="")

def get_move(board: b.Board) -> b.Move:
    """Asks the user to make a move returns it
    >>> get_move(b.make_board())
            Make your move: 1
    (17, 13)
    >>> get_move(b.make_board())
            Make your move: 0
            try again:
    """
    moves = b.legal_moves(board)
    move = int(input("\tMake your move: "))
    while move < 1 or move > len(moves):
        move = int(input("\ttry again: "))
    return moves[move - 1]

def get_mode() -> int:
    """Asks the user to select game mode and returns it
    >>> get_mode()
            Which one is it?: 0
    0
    >>> get_mode()
            Which one is it?: 5
            try again:
    """
    game_mode = int(input("\tWhich one is it?: "))
    while game_mode < 0 or game_mode > 4:
        game_mode = int(input("\ttry again: "))
    return game_mode

def get_choice() -> int:
    """Asks the user about the flow of the game.
    >>> get_choice()
            [1]: Make move
            [0]: Change game mode
            Choose: 0
    0
    >>> get_choice()
            [1]: Make move
            [0]: Change game mode
            Choose: 2
            try again:
    """
    choice = int(input("\t[1]: Make move\n" +  
                       "\t[0]: Change game mode\n" +
                       "\tChoose: "))
    while choice < 0 or choice > 1:
        choice = int(input("\ttry again: "))
    return choice

def _game_result(board: b.Board) -> str:
    """Print the final result of the game in the console.
    >>> _game_result(b.make_board())
    'DRAW'
    >>> _game_result(b.Board(board=[[0, 0, 0, 0, 0], 
                                    [0, 0, 0, 0, 0], 
                                    [0, 0, 0, 1, 0], 
                                    [0, 0, 0, 0, 0], 
                                    [0, 0, 0, 0, 0]], player=2))
    'WHITE wins'
    >>> _game_result(b.Board(board=[[0, 0, 0, 0, 0], 
                                    [0, 0, 0, 0, 0], 
                                    [0, 0, 0, 2, 0], 
                                    [0, 0, 0, 0, 0], 
                                    [0, 0, 0, 0, 0]], player=1))
    'BLACK wins'
    """
    msg = ""
    if (b.black(board) != [] and b.white(board) != []):
        msg = "DRAW"
    elif b.white(board) == []:
        msg = "BLACK wins"
    else:
        msg = "WHITE wins"
    return msg

def _player_color(board: b.Board) -> str:
    """Returns the current player turn.
    >>> _player_color(b.make_board())
    'WHITE'
    """
    if b.white_plays(board):
        return "WHITE"
    else:
        return "BLACK"

def _ai_plays(game_mode: int, board: b.Board) -> bool:
    """Determines whether it's the AI's turn to make a move.
    >>> _ai_plays(1, b.make_board())
    False
    >>> _ai_plays(2, b.make_board())
    False
    >>> _ai_plays(3, b.make_board())
    True
    >>> _ai_plays(4, b.make_board())
    True
    """
    return (game_mode == 4 or 
            (game_mode == 2 and not b.white_plays(board)) or 
            (game_mode == 3 and b.white_plays(board)))

def _board_list(board: b.Board) -> list[str]:
    """Returns a list representation of the board where
    each index corresponds to a position on the board.
    >>> _board_list(b.make_board())
    ['B', 'B', 'B', 'B', 'B',
      'B', 'B', 'B', 'B', 'B',
        'B', 'B', '', 'W', 'W',
          'W', 'W', 'W', 'W', 'W',
            'W', 'W', 'W', 'W', 'W']
    """
    positions = ["" for i in range((25))]
    for pos in b.white(board):
        positions[pos - 1] = "W"
    for pos in b.black(board):
        positions[pos - 1] = "B"
    return positions

def play(game_mode: int, board: b.Board) -> None:
    """Plays alquerque in the console."""
    while b.is_game_over(board) == False and game_mode != 0:
        print(f"\t{_player_color(board)} plays *****************************")
        print_board(board)
        if _ai_plays(game_mode, board):
            move = minimax.next_move(board)
            print(f"\tAI {_player_color(board)} moved from {move[0]} to {move[1]}")
            b.move(move, board)        
        else:
            print("\t------------------------------------------")
            match get_choice():
                case 0:
                    print_menu()
                    game_mode = get_mode()
                    print(f"\tGame mode changed to {game_mode}")
                case 1:
                    print_moves(board)
                    print()
                    move = get_move(board)
                    print(f"\tHUMAN {_player_color(board)} moved from {move[0]} to {move[1]}")
                    b.move(move, board)

def game() -> None:
    print("\t~~~~~~~~ Welcome to Alquerque ~~~~~~~~~")
    board = b.make_board()
    print_menu()
    game_mode = get_mode()
    print()
    play(game_mode, board)
    print("\tFinal state:")
    print_board(board)
    print(f"\t------ GAME OVER ------ result is {_game_result(board)}")
    print("\t**** Thanks for playing Alquerque! ****")

game()
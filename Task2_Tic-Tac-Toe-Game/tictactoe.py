# TIC_TAC_TOE GAME

board_simple = [" ", " ", " ",
                " ", " ", " ",
                " ", " ", " "]

symbols = ["X", "x", "O", "o"]

turn = 1

player_symbol = ""
pc_symbol = ""


def set_pc_symbol():
    global player_symbol, pc_symbol
    symbol = None
    while symbol is None:
        symbol = str(input("Choose X or O: "))

        if symbol not in symbols:
            symbol = None

    player_symbol = symbol.upper()
    for i in range(0, 4, 2):
        if player_symbol != symbols[i]:
            pc_symbol = symbols[i]
            break
    print("=============================")
    print(f"** YOUR SYMBOL IS {player_symbol} **")
    print(f"** COMPUTER SYMBOL IS {pc_symbol} **")
    print("=============================")


def display_board():
    for i in range(0, 9, 3):
        print("| " + board_simple[i] + " | " + board_simple[i + 1] + " | " + board_simple[i + 2] + " | ")
        print("-------------")

    print("=============================")


def user_move():
    global player_symbol

    position = None
    while position is None:
        try:
            position = int(input("Please enter number from 1 to 9: "))

            if position < 1 or position > 9:
                position = None
            else:
                if board_simple[position - 1] == " ":
                    board_simple[position - 1] = player_symbol
                else:
                    print("This position is already taken, try again.\n")
                    position = None

        except ValueError:
            print("Enter an integer number.\n")


def check_winner():
    # Check rows
    for i in range(0, 9, 3):
        if board_simple[i] == board_simple[i + 1] == board_simple[i + 2] and board_simple[i] != " ":
            return True

    # Check columns
    for i in range(3):
        if board_simple[i] == board_simple[i + 3] == board_simple[i + 6] and board_simple[i] != " ":
            return True

    # Check diagonals
    if (board_simple[0] == board_simple[4] == board_simple[8] and board_simple[0] != " ") or \
            (board_simple[2] == board_simple[4] == board_simple[6] and board_simple[2] != " "):
        return True

    return False


def minmax(board, depth, is_maximizing):
    if check_winner() and is_maximizing:
        return -1  # Player wins
    if check_winner() and not is_maximizing:
        return 1  # AI wins
    if " " not in board:
        return 0  # It's a draw

    if is_maximizing:
        max_eval = float("-inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = pc_symbol
                evaluation = minmax(board, depth + 1, False)
                board[i] = " "
                max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = player_symbol
                evaluation = minmax(board, depth + 1, True)
                board[i] = " "
                min_eval = min(min_eval, evaluation)
        return min_eval


def best_move():
    if " " not in board_simple:
        return -1  # Board is full, no valid moves

    best_score = float("-inf")
    best_move_index = -1
    for i in range(9):
        if board_simple[i] == " ":
            board_simple[i] = pc_symbol
            score = minmax(board_simple, 0, False)
            board_simple[i] = " "
            if score > best_score:
                best_score = score
                best_move_index = i
    return best_move_index


def pc_move():
    move = best_move()
    if move > -1:
        board_simple[move] = pc_symbol
    return move


def tic_tac_toe():
    global turn
    print("========= WELCOME TO TIC TAC TOE ===========\n")
    display_board()
    set_pc_symbol()

    while True:
        if not (turn % 2):
            pc_position = pc_move()
            if pc_position == -1:
                print("It's a tie!")
                break
            print(f"The computer chose: {pc_position + 1}")
        elif turn % 2:
            user_move()
        display_board()
        if check_winner():
            if not (turn % 2):
                print("AI wins!")
                break
            else:
                print("Congratulations! You've won!")
                break
        if " " not in board_simple:
            print("It's a tie!")
            break
        turn += 1


tic_tac_toe()

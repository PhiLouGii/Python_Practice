import tkinter
import time
import random
import winsound  # Windows only for sound

# Initialize game variables
playerX = "X"
playerO = "O"
curr_player = playerX
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

color_blue = "#4584b6"
color_yellow = "#ffde57"
color_gray = "#343434"
color_light_gray = "#646464"
color_highlight = "green"

turns = 0
x_wins = 0
o_wins = 0
ties = 0
game_over = False
start_time = None

# Game mode: PvP (Player vs Player) or PvE (Player vs AI)
game_mode = "PvP"

# Functions
def set_tile(row, column):
    global curr_player, game_over, turns

    if game_over or board[row][column]["text"] != "":
        return

    board[row][column]["text"] = curr_player
    highlight_move(row, column)
    play_move_sound()

    check_winner()
    
    if not game_over:
        switch_player()
        if game_mode == "PvE" and curr_player == playerO:
            window.after(500, ai_move)


def switch_player():
    global curr_player
    curr_player = playerX if curr_player == playerO else playerO
    label.config(text=f"{curr_player}'s turn")


def check_winner():
    global game_over, turns, x_wins, o_wins, ties
    turns += 1

    # Check rows, columns, and diagonals
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] != "":
            declare_winner(board[row][0]["text"], [(row, col) for col in range(3)])
            return

    for column in range(3):
        if board[0][column]["text"] == board[1][column]["text"] == board[2][column]["text"] != "":
            declare_winner(board[0][column]["text"], [(row, column) for row in range(3)])
            return

    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
        declare_winner(board[0][0]["text"], [(i, i) for i in range(3)])
        return

    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
        declare_winner(board[0][2]["text"], [(0, 2), (1, 1), (2, 0)])
        return

    # Tie condition
    if turns == 9:
        game_over = True
        ties += 1
        label.config(text="It's a Tie!", foreground=color_yellow)
        update_score()


def declare_winner(winner, winning_tiles):
    global game_over, x_wins, o_wins
    game_over = True
    label.config(text=f"{winner} is the winner!", foreground=color_yellow)
    for row, col in winning_tiles:
        board[row][col].config(foreground=color_yellow, background=color_light_gray)

    if winner == playerX:
        x_wins += 1
    else:
        o_wins += 1

    update_score()


def update_score():
    score_label.config(text=f"X: {x_wins} | O: {o_wins} | Ties: {ties}")


def highlight_move(row, column):
    board[row][column].config(background=color_highlight)


def play_move_sound():
    winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)


def ai_move():
    empty_tiles = [(r, c) for r in range(3) for c in range(3) if board[r][c]["text"] == ""]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        set_tile(row, col)


def new_game():
    global turns, game_over, curr_player
    turns = 0
    game_over = False
    curr_player = playerX
    label.config(text=f"{curr_player}'s turn", foreground="white")

    for row in range(3):
        for column in range(3):
            board[row][column].config(text="", foreground=color_blue, background=color_gray)


def set_mode_pvp():
    global game_mode
    game_mode = "PvP"
    new_game()


def set_mode_pve():
    global game_mode
    game_mode = "PvE"
    new_game()


# Window setup
window = tkinter.Tk()
window.title("Tic Tac Toe")
window.resizable(False, False)
frame = tkinter.Frame(window)

label = tkinter.Label(frame, text=f"{curr_player}'s turn", font=("Consolas", 20), background=color_gray, foreground="white")
label.grid(row=0, column=0, columnspan=3, sticky="we")

# Create board buttons
for row in range(3):
    for column in range(3):
        board[row][column] = tkinter.Button(frame, text="", font=("Consolas", 50, "bold"),
                                             background=color_gray, foreground=color_blue, width=4, height=1,
                                             command=lambda row=row, column=column: set_tile(row, column))
        board[row][column].grid(row=row + 1, column=column)

# Control Buttons
button_restart = tkinter.Button(frame, text="Restart", font=("Consolas", 20), background=color_gray,
                                 foreground="white", command=new_game)
button_restart.grid(row=4, column=0, columnspan=3, sticky="we")

score_label = tkinter.Label(frame, text=f"X: 0 | O: 0 | Ties: 0", font=("Consolas", 14), background=color_gray, foreground="white")
score_label.grid(row=5, column=0, columnspan=3, sticky="we")

button_pvp = tkinter.Button(frame, text="PvP Mode", font=("Consolas", 14), background=color_gray,
                             foreground="white", command=set_mode_pvp)
button_pvp.grid(row=6, column=0, columnspan=1)

button_pve = tkinter.Button(frame, text="PvE Mode", font=("Consolas", 14), background=color_gray,
                             foreground="white", command=set_mode_pve)
button_pve.grid(row=6, column=2, columnspan=1)

frame.pack()

# Center the window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()

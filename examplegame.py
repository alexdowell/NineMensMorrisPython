# Python code for a simple 6-men morris game with AI

import random

# Initializing the board with empty spaces
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
player = 'X'
computer = 'O'
game_over = False


# Function to print the current state of the board
def print_board():
    for line in board:
        print(line)


# Function to check if a player has won
def check_win(char):
    # Check horizontal lines
    for row in board:
        if row.count(char) == 3:
            return True

    # Check vertical lines
    for i in range(3):
        column = [board[j][i] for j in range(3)]
        if column.count(char) == 3:
            return True

    # Check diagonals
    diagonal1 = [board[i][i] for i in range(3)]
    diagonal2 = [board[i][2-i] for i in range(3)]
    if diagonal1.count(char) == 3 or diagonal2.count(char) == 3:
        return True

    return False


# Function to place a piece on the board
def place_piece(char):
    valid_move = False
    while not valid_move:
        row = int(input("Enter row (0-2): "))
        col = int(input("Enter col (0-2): "))
        if board[row][col] == ' ':
            board[row][col] = char
            valid_move = True
        else:
            print("Invalid move, try again.")
    if check_win(char):
        print(char + " wins!")
        global game_over
        game_over = True


# Function for the computer's turn
def computer_move():
    valid_move = False
    while not valid_move:
        # Generate a random move
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == ' ':
            board[row][col] = computer
            valid_move = True
    if check_win(computer):
        print(computer + " wins!")
        global game_over
        game_over = True


# Game loop
print_board()
while not game_over:
    place_piece(player)
    print_board()
    if not game_over:
        computer_move()
        print("Computer's move:")
        print_board()
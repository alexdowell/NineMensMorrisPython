import os
import pickle
import sys
import time
import pygame
from NineMensMorris_Game import Game

DEBUG = False

# Check if the load_game.txt file exists and create it if it doesn't
load_file_path = "load_game.txt"
if not os.path.exists(load_file_path):
    with open(load_file_path, "w+") as variable_load_file:
        variable_load_file.write('False')

# Read data from load_game.txt
with open(load_file_path, "r") as variable_load_file:
    variable_load = variable_load_file.read()

# Set up the new board
board_size = 9
computer = 0

# Extract board size from the system (from the previous screen)
if len(sys.argv) > 1:
    board_size_comm = sys.argv[1]
    board_size = int(board_size_comm[0])
    computer = int(board_size_comm[1])

# Global Variables
board = Game()

# Set up the board
board.set_board_size(board_size)
board.set_initial_positions()
board.set_player_turn(1)
board.set_initial_remaining_turns()
board.set_initial_permissible_moves()
board.set_game_mode(computer)

# Initialize pygame
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 18)

# Set up the screen
screen = pygame.display.set_mode((600, 750))
pygame.display.set_caption("Nine Men Morris")

# Load nine mens morris board images
boardImg3 = pygame.image.load('3mens.png')
boardImg6 = pygame.image.load('6mens.png')
boardImg9 = pygame.image.load('dragon9mens.png')

# Load avatar images
leafImg = pygame.image.load('player1_30x30.png')
fireImg = pygame.image.load('player2_30x30.png')
highImg = pygame.image.load('high.png')
roboImg = pygame.image.load('robo1.png')
pantherimg = pygame.image.load('panther.png')
pantherimg = pygame.transform.scale(pantherimg, (30, 30))
dragonimg = pygame.image.load('dragon.png')
dragonimg = pygame.transform.scale(dragonimg, (30, 30))

# Load buttons and adjust sizes
restart_button = pygame.transform.scale(pygame.image.load('restart.png'), (30, 30))
play_button = pygame.transform.scale(pygame.image.load('play_button.png'), (30, 30))
pause_button = pygame.transform.scale(pygame.image.load('pause_button.png'), (30, 30))
rewind_button = pygame.transform.scale(pygame.image.load('rewind_button.png'), (30, 30))
fast_forward_button = pygame.transform.scale(pygame.image.load('fast_forward_button.png'), (30, 30))
back_button = pygame.transform.scale(pygame.image.load('back_button.png'), (30, 30))
replay_button = pygame.transform.scale(pygame.image.load('replay_button.png'), (30, 30))
save_button = pygame.transform.scale(pygame.image.load('save_button.png'), (30, 30))
load_button = pygame.transform.scale(pygame.image.load('load_button.png'), (30, 30))

# Expand the size of 3 mens and 6 mens boards
boardImg3 = pygame.transform.scale(boardImg3, (500, 500))
boardImg6 = pygame.transform.scale(boardImg6, (500, 500))
boardImg9 = pygame.transform.scale(boardImg9, (500, 500))

# Game mode selection buttons
single_player = pygame.transform.scale(pygame.image.load('single_player.png'), (30, 30))
multi_player = pygame.transform.scale(pygame.image.load('multi_player.png'), (30, 30))

coords = {}
if(board.get_board_size() == 9):
    coords = {
        0: (22, 22), # positions 0-23 are the 24 positions on the board
        1: (230, 22),
        2: (450, 22),
        3: (22, 240),
        4: (450, 240),
        5: (22, 450),
        6: (230, 450),
        7: (450, 450),
        8: (95, 95),
        9: (230, 95),
        10: (380, 95),
        11: (95, 240),
        12: (380, 240),
        13: (95, 378),
        14: (230, 378),
        15: (380, 378),
        16: (162, 169),
        17: (230, 169),
        18: (308, 169),
        19: (162, 240),
        20: (308, 240),
        21: (162, 308),
        22: (230, 308),
        23: (308, 308),
        24: (550,22), # replay button
        25: (550, 122), # save button
        26: (550, 222), # load button
        27: (550, 322) # restart button
    }
elif(board.get_board_size() == 6):
    coords = {
        0: (12, 16),
        1: (235, 16),
        2: (460, 16),
        3: (125, 130),
        4: (235, 130),
        5: (348, 130),
        6: (12, 240),
        7: (125, 240),
        8: (348, 240),
        9: (460, 240),
        10: (125, 350),
        11: (235, 350),
        12: (348, 350),
        13: (12, 463),
        14: (235, 463),
        15: (460, 463),
        16: (550, 22), # replay button
        17: (550, 122), # save button
        18: (550, 222), # load button
        19: (550, 322) # restart button
    }
elif(board.get_board_size() == 3):
    coords = {
        0: (33, 34),
        1: (238, 34),
        2: (443, 34),
        3: (33, 240),
        4: (238, 240),
        5: (445, 240),
        6: (33, 443),
        7: (238, 443),
        8: (445, 443),
        9: (550, 22), # replay button
        10: (550, 122), # save button
        11: (550, 222), # load button
        12: (550, 322) # restart button
    }

replay_coords = {
    1: (22, 550),  # rewind a move button
    2: (169, 550), # play button
    3: (450, 550), # fast forward button
    4: (550, 550), # back button
}
play_coords = {
    1: (169, 550),  # play button
    2: (308, 550), # pause button
    3: (550, 550), # back button
}
selection_coords = {
    1: (22, 550),  # single player
    2: (169, 550), # multiplayer
}
selection_clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in selection_coords.values()]
play_clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in play_coords.values()]
replay_clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in replay_coords.values()]
clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in coords.values()]
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Functions to draw the game state
def draw_board(screen, board_img, positions, coords, replay, play, game_mode_selection, startpos):
    try:
        # Draw the background board
        screen.blit(board_img.convert(), (0, 0))

        # Draw borders around the clickable areas
        if DEBUG and not (replay and play):
            clickables_to_draw = replay_clickables if replay else clickables
            for rect in clickables_to_draw:
                pygame.draw.rect(screen, BLACK, rect, 1)

        # Draw the pieces on the board
        for pos, value in enumerate(positions):
            x, y = coords[pos]
            piece_img = pantherimg.convert_alpha() if value == 1 else dragonimg.convert_alpha()
            screen.blit(piece_img, (x, y))

        # Highlight selected piece with a green rectangle
        if startpos is not None:
            x, y = coords[startpos]
            pygame.draw.rect(screen, GREEN, (x, y, 30, 30), 3)

        # Draw the selection buttons for game mode
        if game_mode_selection:
            screen.blit(single_player.convert_alpha(), (selection_coords[1]))
            screen.blit(multi_player.convert_alpha(), (selection_coords[2]))

        # Draw replay and other buttons based on the game state
        draw_buttons(screen, replay, play)
    except Exception as e:
        print(f"Error drawing the board: {e}")

def draw_buttons(screen, replay, play):
    replay_button_coord = None
    save_button_coord = None
    load_button_coord = None
    restart_button_coord = None

    if not (replay and play):
        replay_button_coord, save_button_coord, load_button_coord, restart_button_coord = get_replay_restart_button_coords()

        screen.blit(replay_button.convert_alpha(), replay_button_coord)
        screen.blit(save_button.convert_alpha(), save_button_coord)
        screen.blit(load_button.convert_alpha(), load_button_coord)
        screen.blit(restart_button.convert_alpha(), restart_button_coord)

    elif replay and not play:
        rewind_button_coord, play_button_coord, fast_forward_button_coord, back_button_coord = replay_coords[1:]

        screen.blit(rewind_button.convert_alpha(), rewind_button_coord)
        screen.blit(play_button.convert_alpha(), play_button_coord)
        screen.blit(fast_forward_button.convert_alpha(), fast_forward_button_coord)
        screen.blit(back_button.convert_alpha(), back_button_coord)

    elif replay and play:
        play_button_coord, pause_button_coord, back_button_coord = play_coords[1:]

        screen.blit(play_button.convert_alpha(), play_button_coord)
        screen.blit(pause_button.convert_alpha(), pause_button_coord)
        screen.blit(back_button.convert_alpha(), back_button_coord)

def get_replay_restart_button_coords():
    if board.get_board_size() == 3:
        return coords[9], coords[10], coords[11], coords[12]
    elif board.get_board_size() == 6:
        return coords[16], coords[17], coords[18], coords[19]
    elif board.get_board_size() == 9:
        return coords[24], coords[25], coords[26], coords[27]

def draw_game_info(screen, game_functions, gameover, gridlocked, removepos, replay, game_mode_selection):
    texts = []

    if gameover:
        if replay:
            texts = ["In Replay Mode"]
        elif gridlocked:
            texts = [
                f"Player {2 if game_functions.get_player_turn() == 1 else 1} is gridlocked! Player {2 if game_functions.get_player_turn() == 1 else 1} wins!",
                "Close window to change game settings or click Restart"
            ]
        else:
            texts = [
                f"Game Over! Player {2 if game_functions.get_player_turn() == 1 else 1} wins!",
                "Close window to change game settings or click Restart"
            ]
    elif not gameover and not game_mode_selection:
        if game_functions.get_remaining_turns() != 0:
            if removepos:
                texts = [
                    f"Player {1 if game_functions.get_player_turn() == 1 else 2} formed a mill!",
                    "Select an opponent's piece to remove from the board."
                ]
            elif replay:
                texts = ["In Replay Mode"]
            else:
                texts = [
                    f"It's Player {1 if game_functions.get_player_turn() == 1 else 2}'s turn!",
                    f"Remaining Turns: {game_functions.get_remaining_turns()}"
                ]
        elif game_functions.get_remaining_turns() == 0:
            if removepos:
                texts = [
                    f"Player {1 if game_functions.get_player_turn() == 1 else 2} formed a mill!",
                    "Select an opponent's piece to remove from the board."
                ]
            elif replay:
                texts = ["In Replay Mode"]
            else:
                texts = [
                    f"It's Player {1 if game_functions.get_player_turn() == 1 else 2}'s turn!",
                    "It's time to move pieces! Select a piece to move then select the position you want to move to."
                ]
    elif game_mode_selection:
        texts = ["Select Game Mode"]

    for i, text in enumerate(texts):
        textsurface = myfont.render(text, False, BLACK)
        screen.blit(textsurface, (10, 600 + i * 30))


'''
# Functions to draw the game state
def draw_board(screen, board_img, positions, coords, replay, play, game_mode_selection, startpos):
    try:
        # Draw the background board
        screen.blit(board_img.convert(), (0, 0))
        # Draw boarders around the clickable areas
        if DEBUG:
            if replay == False and play == False:
                for rect in clickables:
                    pygame.draw.rect(screen, BLACK, rect, 1)
            if replay == True and play == False:
                for rect in replay_clickables:
                    pygame.draw.rect(screen, BLACK, rect, 1)
            if replay == True and play == True:
                for rect in play_clickables:
                    pygame.draw.rect(screen, BLACK, rect, 1)
            print("positions in draw_board: ", positions)
        # Draw the pieces on the board
        for pos, value in enumerate(positions):
            x, y = coords[pos]
            if value == 1:
                screen.blit(pantherimg.convert_alpha(), (x, y))
            elif value == 2:
                screen.blit(dragonimg.convert_alpha(), (x, y))

        #Highlight with green rectangle the selected piece
        if startpos != None:
            x, y = coords[startpos]
            pygame.draw.rect(screen, GREEN, (x, y, 30, 30), 3)

        # draw the selection buttons
        if game_mode_selection == True:
            screen.blit(single_player.convert_alpha(), (selection_coords[1]))
            screen.blit(multi_player.convert_alpha(), (selection_coords[2]))



        # Draw replay button
        if replay == False and play == False:
            replay_btn_coord = None
            save_btn_coord = None
            load_btn_coord = None
            restart_btn_coord = None
            if(board.get_board_size() == 3):
                replay_btn_coord = coords[9]
                save_btn_coord = coords[10]
                load_btn_coord = coords[11]
                restart_btn_coord = coords[12]
            elif(board.get_board_size() == 6):
                replay_btn_coord = coords[16]
                save_btn_coord = coords[17]
                load_btn_coord = coords[18]
                restart_btn_coord = coords[19]
            elif(board.get_board_size() == 9):
                replay_btn_coord = coords[24]
                save_btn_coord = coords[25]
                load_btn_coord = coords[26]
                restart_btn_coord = coords[27]
            screen.blit(replay_button.convert_alpha(), (replay_btn_coord))
            screen.blit(save_button.convert_alpha(), (save_btn_coord))
            screen.blit(load_button.convert_alpha(), (load_btn_coord))
            screen.blit(restart_button.convert_alpha(), (restart_btn_coord))
        if replay == True and play == False:
            screen.blit(rewind_button.convert_alpha(), (replay_coords[1]))
            screen.blit(play_button.convert_alpha(), (replay_coords[2]))
            screen.blit(fast_forward_button.convert_alpha(), (replay_coords[3]))
            screen.blit(back_button.convert_alpha(), (replay_coords[4]))
        if replay == True and play == True:
            screen.blit(play_button.convert_alpha(), (play_coords[1]))
            screen.blit(pause_button.convert_alpha(), (play_coords[2]))
            screen.blit(back_button.convert_alpha(), (play_coords[3]))
    except Exception as e:
        print(f"Error drawing the board: {e}")







def draw_game_info(screen, game_functions, gameover, gridlocked, removepos, replay, game_mode_selection):

    # Display the variables from the Board class
    if gameover:
        if(replay):
            texts = [
                f"In Replay Mode"
            ]
        elif(gridlocked):
            texts = [
                f"Player {2 if game_functions.get_player_turn() == 1 else 1} is gridlocked! Player {2 if game_functions.get_player_turn() == 1 else 1} wins!",
                f"Close window to change game settings or click Restart"
            ]
        else:
            texts = [
                f"Game Over! Player {2 if game_functions.get_player_turn() == 1 else 1} wins!",
                f"Close window to change game settings or click Restart"
            ]
    if not gameover and not game_mode_selection:
        if(game_functions.get_remaining_turns() != 0):
            if(removepos):
                texts = [
                    f"Player {1 if game_functions.get_player_turn() == 1 else 2} formed a mill!",
                    f"Select an opponent's piece to remove from the board."
                ]
            elif(replay):
                texts = [
                    f"In Replay Mode"
                ]
            else:
                texts = [
                    f"It's Player {1 if game_functions.get_player_turn() == 1 else 2}'s turn!",
                    f"Remaining Turns: {game_functions.get_remaining_turns()}"
                ]

        elif(game_functions.get_remaining_turns() == 0):
            if(removepos):
                texts = [
                    f"Player {1 if game_functions.get_player_turn() == 1 else 2} formed a mill!",
                    f"Select an opponent's piece to remove from the board."
                ]
            elif(replay):
                texts = [
                    f"In Replay Mode"
                ]
            else:
                texts = [
                    f"It's Player {1 if game_functions.get_player_turn() == 1 else 2}'s turn!",
                    f"It's time to move pieces! Select a piece to move then select the position you want to move to."
                ]
    if game_mode_selection:
        texts = [
            f"Select Game Mode"
        ]


    for i, text in enumerate(texts):
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface, (10, 600 + i*30))
'''

###### replay with GUI ######
def set_replay():
    print("replay function called")
    if not os.path.exists(board.TEMP_LOG_PATH):
        print("No saved game states to replay.")
        return

    with open(board.TEMP_LOG_PATH, "rb") as file:
        log = pickle.load(file)

    if not log:
        print("Log is empty. Nothing to replay.")
        return

    # Save current state
    current_state = {
        'board_size': board.get_board_size(),
        'positions': board.get_positions(),
        'player_turn': board.get_player_turn(),
        'active_mills': board.get_active_mills(),
        'remaining_turns': board.get_remaining_turns(),
        'permissible_moves': board.get_permissible_moves(),
        'game_mode': board.get_game_mode()
    }
    currentstuff = [log,current_state]
    return currentstuff

def replay_handler(replay_option,log,replay_state,current_state):
    print("replay_option: ", replay_option)
    print("replay_state: ", replay_state)
    print("current_state: ", current_state)
    index = replay_state
    if log is None or current_state is None:
        print("Error: Log or current state is None")
        return
    if replay_option == 0: # rewind a move button
        if index != 0:
            index -= 1
            replay_state = index
        else:
            index = 0
            replay_state = index
        state = log[index]
        board.set_board_size(state['board_size'])
        board.set_positions(state['positions'])
        board.set_player_turn(state['player_turn'])
        board.set_active_mills(state['active_mills'])
        board.set_remaining_turns(state['remaining_turns'])
        board.set_game_mode(state['game_mode'])
        return replay_state

    if replay_option == 2:
        if index != (len(log)-1): # fast forward button
            index += 1
            replay_state = index
        else:
            index = 0
            replay_state = index
        print("log length: ", len(log))
        print("index: ", index)
        state = log[index]
        board.set_board_size(state['board_size'])
        board.set_positions(state['positions'])
        board.set_player_turn(state['player_turn'])
        board.set_active_mills(state['active_mills'])
        board.set_remaining_turns(state['remaining_turns'])
        board.set_game_mode(state['game_mode'])
        return replay_state
    
    if replay_option == 3: # exit replay button
        #reset current state
        current_state = current_state
        board.set_board_size(state['board_size'])
        board.set_positions(current_state['positions'])
        board.set_player_turn(current_state['player_turn'])
        board.set_active_mills(current_state['active_mills'])
        board.set_remaining_turns(current_state['remaining_turns'])
        board.set_game_mode(state['game_mode'])


def handle_mouse_up_events(event, replay, startpos, endpos, gameover, currentstuff, clickables, replay_clickables):
    try:
        if replay:
            handle_replay_mouse_up(event, replay, currentstuff, replay_clickables)
        else:
            handle_main_game_mouse_up(event, startpos, endpos, gameover, currentstuff, clickables)
    except Exception as e:
        print(f"Error handling mouse up events: {e}")

def handle_main_game_mouse_up(event, currentstuff, clickables):
    try:
        for i, rect in enumerate(clickables):
            if rect.collidepoint(event.pos):
                handle_main_game_click(i, currentstuff)
                break
    except Exception as e:
        print(f"Error handling main game mouse up event: {e}")
def handle_replay_mouse_up(event, currentstuff, replay_clickables):
    try:
        for i, rect in enumerate(replay_clickables):
            if rect.collidepoint(event.pos):
                handle_replay_click(i, currentstuff)
                break
    except Exception as e:
        print(f"Error handling replay mouse up event: {e}")

def handle_main_game_click(index, replay, currentstuff):
    payload = None
    try:
        # Handle main game clicks based on the index
        # DEBUG print(f"Main game click: {index}")
        # Add logic here
        if board_size == 9:
            if index == 24:
                currentstuff = set_replay(index)
                replay = True
                payload = currentstuff
            elif(index == 25):
                board.save()
            elif(index == 26):
                board.load()
            elif(index == 27):
                board.new_restart_game()
                gameover = False
    except Exception as e:
        print(f"Error handling main game click: {e}")

def handle_replay_click(index, replay, currentstuff):
    try:
        # Handle replay clicks based on the index and current state
        # DEBUG print(f"Replay click: {index}")
        replay_handler(index, currentstuff[0], currentstuff[1], currentstuff[2])
    except Exception as e:
        print(f"Error handling replay click: {e}")


def game_loop(variable_load):
    # DEBUG print("Initializing game window")
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    running = True
    startpos, endpos, removepos, gameover, gridlocked, replay = None, None, False, False, False, False
    replay_state, play, pause, sleep, boardImg = 0, False, False, False, None
    game_mode_selection = False

    while running:
        try:
            # Event handling
            if not game_mode_selection:
                if not play:
                    for event in pygame.event.get():
                        # DEBUG print(f"Event: {event}")
                        if event.type == pygame.QUIT:
                            # DEBUG print("Quit event detected. Closing game window...")
                            running = False
                            break
                        if event.type == pygame.MOUSEBUTTONUP:
                            handle_mouse_up_events(event, replay, startpos, endpos, gameover, currentstuff, clickables, replay_clickables)
                if play:
                        handle_play_events(event, play_clickables, currentstuff, play_loop, play_length, play_length, counter)
                
            if game_mode_selection:
                handle_game_mode_selection(pygame.event.get(), selection_clickables, board, game_mode_selection)
            
            handle_computer_turn(board, startpos, endpos, removepos, gameover)
            
            screen.fill(WHITE)
            boardImg = choose_board_image(board, boardImg9, boardImg6, boardImg3)
            draw_board(screen, boardImg, board.get_positions(), coords, replay, play, game_mode_selection, startpos)
            if sleep:
                time.sleep(1)
                sleep = False
            draw_game_info(screen, board, gameover, gridlocked, removepos, replay, game_mode_selection)
            pygame.display.flip()
            clock.tick(60)
        except Exception as e:
            print(f"Error in game loop: {e}")
            running = False
'''
def game_loop(variable_load):

    print("Initializing game window...")
    screen.fill(WHITE)
    clock = pygame.time.Clock()

    #print("Entering main game loop...")

    running = True
    startpos = None
    endpos = None
    removepos = False
    gameover = False
    gridlocked = False
    replay = False
    replay_state = 0
    play = False
    pause = False
    sleep = False
    boardImg = None
    game_mode_selection = False
    while running:
        try:
            # Event handling
            if game_mode_selection == False:
                if play == False:
                    for event in pygame.event.get():
                        print(f"Event: {event}")  # This will print out each event captured
                        if event.type == pygame.QUIT:
                            print("Quit event detected. Closing game window...")
                            running = False
                            break
                        #print("event.type: ", event.type)
                        #print("pygame.MOUSEBUTTONUP: ", pygame.MOUSEBUTTONUP)
                        if event.type == pygame.MOUSEBUTTONUP:
                            if replay == True:
                                for idx, rect in enumerate(replay_clickables):
                                    # print("the replay clickables are: ", enumerate(replay_coords))
                                    # print("The idx is: ", idx)
                                    # print("The rect is: ", rect)
                                    # print("here replay")
                                    # print("event.pos: ", event.pos)
                                    if rect.collidepoint(event.pos):
                                        if idx == 0: # rewind a move button
                                            #print("here rewind")
                                            replay_state = replay_handler(idx, currentstuff[0], replay_state, currentstuff[1])
                                            break
                                        if idx == 1: # play button
                                            #print("here play")
                                            play_loop = 0
                                            play = True
                                            play_length = len(currentstuff[0])
                                            counter = time.time()
                                            break

                                        if idx == 2: # fast forward
                                            #print("here fast forward")
                                            replay_state = replay_handler(idx  , currentstuff[0], replay_state, currentstuff[1])
                                            break
                                        if idx == 3: # exit replay button
                                            #print("here exit replay")
                                            replay_handler(idx  , currentstuff[0],  replay_state, currentstuff[1])
                                            replay = False
                                            break
                            if replay == False:
                                for idx, rect in enumerate(clickables):
                                    # print("the clickables are: ", enumerate(clickables))
                                    # print("The idx is: ", idx)
                                    # print("The rect is: ", rect)
                                    # print("here1")
                                    # print("event.pos: ", event.pos)
                                    if rect.collidepoint(event.pos):
                                        if(board.get_board_size() == 9):
                                            if(idx == 24):
                                                currentstuff = set_replay(idx)
                                                replay = True
                                                break
                                            elif(idx == 25):
                                                board.save()
                                                break
                                            elif(idx == 26):
                                                board.load()
                                                break
                                            elif(idx == 27):
                                                board.new_restart_game()
                                                gameover = False
                                                break
                                        elif(board.get_board_size() == 6):
                                            if(idx == 16):
                                                currentstuff = set_replay(idx)
                                                replay = True
                                                break
                                            elif(idx == 17):
                                                board.save()
                                                break
                                            elif(idx == 18):
                                                board.load()
                                                break
                                            elif(idx == 19):
                                                board.new_restart_game()
                                                gameover = False
                                                break
                                        elif(board.get_board_size() == 3):
                                            if(idx == 9):
                                                currentstuff = set_replay(idx)
                                                replay = True
                                                break
                                            elif(idx == 10):
                                                board.save()
                                                break
                                            elif(idx == 11):
                                                board.load()
                                                break
                                            elif(idx == 12):
                                                board.new_restart_game()
                                                gameover = False
                                                break
                                        if removepos == True:
                                            if board.form_mill(idx):
                                                board.check_remove_active_mill()
                                                removepos = False
                                                board.save_current_state_to_log()
                                                if (board.is_game_over() or board.is_gridlocked()) and (board.get_board_size() == 6 or board.get_board_size() == 9) and board.get_remaining_turns() == 0:
                                                    gameover = True
                                                    gridlocked = True
                                                break
                                            break
                                        if board.get_remaining_turns() != 0:
                                            #print("here2")
                                            #print(f"Clicked on position: {idx}")
                                            if board.place_piece(idx):
                                                board.check_remove_active_mill()
                                                #print("here passed place piece")
                                                if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                                                    removepos = True
                                                    break
                                                elif board.form_mill_GUI() and board.get_board_size() == 3:
                                                    #print("Game over!")
                                                    board.save_current_state_to_log()
                                                    #print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                                                    gameover = True
                                                    break
                                                board.save_current_state_to_log()
                                                #print("Form mill GUI = ", board.form_mill_GUI())
                                                #print("Board size: ", board.get_board_size())
                                                break
                                        if board.get_remaining_turns() == 0:
                                                if board.is_game_over() or board.is_gridlocked():
                                                    #print("Game over!")
                                                    #print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                                                    gameover = True
                                                    gridlocked = True
                                                    break
                                                if startpos == None:
                                                    startpos = idx
                                                    #print("startpos: ", startpos)
                                                    #print("Starting position (piece selected to move): ", startpos)
                                                    break
                                                else:
                                                    if startpos == idx:
                                                        break
                                                    endpos = idx
                                                    #print("Ending position (position to move to): ", endpos)
                                                    #print("endpos: ", endpos)
                                                    if board.player_piece_count() == 3 and (board.get_board_size() == 6 or board.get_board_size() == 9):
                                                        if board.fly_piece(startpos, endpos):
                                                            board.check_remove_active_mill()
                                                            if board.form_mill_GUI():
                                                                removepos = True
                                                                startpos = None
                                                                endpos = None
                                                                break
                                                            board.save_current_state_to_log()
                                                            startpos = None
                                                            endpos = None
                                                            break
                                                        else:
                                                            startpos = None
                                                            endpos = None
                                                    else:
                                                        if board.move_piece(startpos, endpos):
                                                            print("Moved piece from ", startpos, "to ", endpos)
                                                            board.check_remove_active_mill()
                                                            if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                                                                removepos = True
                                                                startpos = None
                                                                endpos = None
                                                                break
                                                            elif board.form_mill_GUI() and board.get_board_size() == 3:
                                                                #print("Game over!")
                                                                board.save_current_state_to_log()
                                                                #print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                                                                gameover = True
                                                                break
                                                            board.save_current_state_to_log()
                                                            startpos = None
                                                            endpos = None
                                                            break
                                                        else:
                                                            startpos = None
                                                            endpos = None
                if play == True:
                    for event in pygame.event.get():
                        print(f"Event: {event}")  # This will print out each event captured
                        if event.type == pygame.QUIT:
                            print("Quit event detected. Closing game window...")
                            running = False
                            break
                            
                        print("event.type: ", event.type)
                        if event.type == pygame.MOUSEBUTTONUP:
                            for idx, rect in enumerate(play_clickables):
            
                                # print("the replay clickables are: ", enumerate(replay_coords))
                                # print("The idx is: ", idx)
                                # print("The rect is: ", rect)
                                # print("here1")
                                # print("event.pos: ", event.pos)
                                if rect.collidepoint(event.pos):
                                    if idx == 0:
                                        pause = False
                                        counter = time.time()
                                        break
                                    if idx == 1:
                                        pause = True
                                        pause_play_loop = play_loop
                                        break
                                    if idx == 2:
                                        play = False
                                        break
                    if play_loop == (play_length-1):
                        counter = time.time()
                        sleep = True
                    state = currentstuff[0][play_loop]
                    board.set_board_size(state['board_size'])
                    board.set_positions(state['positions'])
                    board.set_player_turn(state['player_turn'])
                    board.set_active_mills(state['active_mills'])
                    board.set_remaining_turns(state['remaining_turns'])
                    board.set_permissible_moves(state['permissible_moves'])
                    if pause == True:
                        play_loop = pause_play_loop
                    if pause == False:
                        play_loop = round( time.time() - counter )
            
                if board.get_player_turn() == 2 and board.get_game_mode() == 1:
                    if board.get_remaining_turns() != 0:
                        board.computer_place_piece()

                        if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                            removepos = True
                            remove_piece = board.computer_remove_piece()

                        if board.form_mill_GUI() and board.get_board_size() == 3:
                            print("Game over!")
                            print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                            gameover = True
                            break

                        if removepos == True:
                            if board.form_mill(remove_piece):
                                removepos = False
                                board.check_remove_active_mill()
                                break
                            break
                    if board.get_remaining_turns() == 0:
                        if board.player_piece_count() != 3:
                            board.computer_move_piece()
                        if board.player_piece_count() == 3 and (board.get_board_size() == 6 or board.get_board_size() == 9):
                            board.computer_fly_piece() # gotta write the method for this

                        if board.form_mill_GUI() and (board.get_board_size() == 6 or board.get_board_size() == 9):
                            removepos = True
                            remove_piece = board.computer_remove_piece()
                            #print("remove piece on: ", removepos)
                            #print("and the remove piece is: ", remove_piece)

                        if board.form_mill_GUI() and board.get_board_size() == 3:
                            gameover = True
                            break

                        if removepos == True:
                            if board.form_mill(remove_piece):
                                removepos = False
                                board.check_remove_active_mill()
                                break
                            break
                        #print(f"Player Turn is: {2 if board.get_player_turn() == 2 else 1}")
                    board.save_current_state_to_log()
                

            if game_mode_selection == True:
                for event in pygame.event.get():
                    print(f"Event: {event}")  # This will print out each event captured
                    if event.type == pygame.QUIT:
                        print("Quit event detected. Closing game window...")
                        running = False
                        break
                    #print("event.type: ", event.type)
                    #print("pygame.MOUSEBUTTONUP: ", pygame.MOUSEBUTTONUP)
                    if event.type == pygame.MOUSEBUTTONUP:
                        for idx, rect in enumerate(selection_clickables):
                            if rect.collidepoint(event.pos):
                                if idx == 0:    
                                    board.set_game_mode(1)
                                    game_mode_selection = False
                                    break
                                if idx == 1:
                                    board.set_game_mode(0)
                                    game_mode_selection = False
                                    break


            #print("startpos: ", startpos)
            #print("endpos: ", endpos)
            #print("removepos: ", removepos)
            #print("gameover: ", gameover)
            #print("Print test: ", test)
            # print("replay: ", replay)
            # print("play: ", play)
            # print("board positions: ", board.get_positions())
            #print("board player turn (after computer turn): ", board.get_player_turn())
            #print("Loop check: ", loop_check)
            #print("computer move from: ", selections[0])
            #print("computer move to: ", selections[1])
            #print("board positions: ", board.get_positions())
            #     # Add more event handling logic here for other phases
            # print("remaining turns: ", board.get_remaining_turns())
            # Drawing the game state
            #print("Calling draw_board()...")

            #print("Computer: ", computer)

            if variable_load == 'True':
                board.load()
                
                # save load == false in load_game.txt
                variable_load = open("load_game.txt", "w+")
                variable_load.write('False')
                variable_load.close()

                variable_load = 'False'

                game_mode_selection = True



                print(f'This is: {variable_load}')

                # open("load_game.txt", "r")
                # variable_load = variable_load.read()
                # print(variable_load)
            
            screen.fill(WHITE)
            if(board.get_board_size() == 9):
                boardImg = boardImg9
            elif(board.get_board_size() == 6):
                boardImg = boardImg6
            elif(board.get_board_size() == 3):
                boardImg = boardImg3
            
            draw_board(screen, boardImg, board.get_positions(), coords, replay, play, game_mode_selection, startpos)
            if sleep == True:
                time.sleep(1)
                sleep = False
            
            #print("Calling draw_game_info()...")
            draw_game_info(screen, board, gameover, gridlocked, removepos, replay, game_mode_selection)

            # Updating the display
            #print("Updating display...")
            pygame.display.flip()

            # Frame rate
            clock.tick(60)
            
        except Exception as e:
            print(f"Error in game loop: {e}")
            running = False

    print("Exiting game...")

    pygame.quit()
    sys.exit()



'''



game_loop(variable_load)
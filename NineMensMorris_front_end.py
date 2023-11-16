import os
import pickle
import sys
import time

import pygame
from NineMensMorris_version7 import Game_Functions as Game_Functions

DEBUG = True
# Global Variables
board = Game_Functions()
pygame.font.init()  # you have to call this at the start, 
                    # if you want to use this module.
myfont = pygame.font.SysFont('Arial', 18)
# Initialize pygame
print(" calling pygame.init()")
pygame.init()
print("pygame initialized")
# Set the size of the screen
screen = pygame.display.set_mode((600, 750))

pygame.display.set_caption("Nine Men Morris")
print("game window initialized")
# nine mens morris board image 
boardImg = pygame.image.load('morrisbig.png') 
# avatar images
leafImg = pygame.image.load('player1_30x30.png')
fireImg = pygame.image.load('player2_30x30.png')
highImg = pygame.image.load('high.png')
roboImg = pygame.image.load('robo1.png')
# replay buttons
play_button = pygame.image.load('play_button.png')
pause_button = pygame.image.load('pause_button.png')
rewind_button = pygame.image.load('rewind_button.png')
fast_forward_button = pygame.image.load('fast_forward_button.png')
back_button = pygame.image.load('back_button.png')
replay_button = pygame.image.load('replay_button.png')
# rduce size of of the replay button images
play_button = pygame.transform.scale(play_button, (30, 30))
pause_button = pygame.transform.scale(pause_button, (30, 30))
rewind_button = pygame.transform.scale(rewind_button, (30, 30))
fast_forward_button = pygame.transform.scale(fast_forward_button, (30, 30))
back_button = pygame.transform.scale(back_button, (30, 30))
replay_button = pygame.transform.scale(replay_button, (30, 30))
# coordinates of each board position in Board and corresponding position in the nine mens morris board image
print("images loaded")
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
play_clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in play_coords.values()]
replay_clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in replay_coords.values()]
clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in coords.values()]
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Functions to draw the game state
def draw_board(screen, board_img, positions, coords,replay,play):
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
                screen.blit(leafImg.convert_alpha(), (x, y))
            elif value == 2:
                screen.blit(fireImg.convert_alpha(), (x, y))
        # Draw replay button
        if replay == False and play == False:
            screen.blit(replay_button.convert_alpha(), (coords[24]))
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

def draw_game_info(screen, game_functions, gameover):
    # Display the variables from the Board class
    if gameover == True:
        texts = [
        f"Game Over! Player {2 if game_functions.get_player_turn() == 1 else 1} wins!"
    ]
    if gameover == False:
        texts = [
            f"Positions: {game_functions.get_positions()}",
            f"Player Turn: {game_functions.get_player_turn()}",
            f"Active Mills: {game_functions.get_active_mills()}",
            f"Remaining Turns: {game_functions.get_remaining_turns()}",
        ]

    for i, text in enumerate(texts):
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface, (10, 600 + i*30))

###### replay with GUI ######
def set_replay(idx):
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
        'positions': board.get_positions(),
        'player_turn': board.get_player_turn(),
        'active_mills': board.get_active_mills(),
        'remaining_turns': board.get_remaining_turns(),
        'permissible_moves': board.get_permissible_moves()
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
        board.set_positions(state['positions'])
        board.set_player_turn(state['player_turn'])
        board.set_active_mills(state['active_mills'])
        board.set_remaining_turns(state['remaining_turns'])
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
        board.set_positions(state['positions'])
        board.set_player_turn(state['player_turn'])
        board.set_active_mills(state['active_mills'])
        board.set_remaining_turns(state['remaining_turns'])
        return replay_state
    
    if replay_option == 3: # exit replay button
        #reset current state
        current_state = current_state
        board.set_positions(current_state['positions'])
        board.set_player_turn(current_state['player_turn'])
        board.set_active_mills(current_state['active_mills'])
        board.set_remaining_turns(current_state['remaining_turns'])

def game_loop():

    print("Initializing game window...")
    screen.fill(WHITE)
    clock = pygame.time.Clock()

    print("Entering main game loop...")
    running = True
    startpos = None
    endpos = None
    removepos = False
    gameover = False
    replay = False
    replay_state = 0
    play = False
    pause = False
    sleep = False
    while running:
        try:
            # Event handling
            if play == False:
                for event in pygame.event.get():

                    print(f"Event: {event}")  # This will print out each event captured
                    if event.type == pygame.QUIT:
                        print("Quit event detected. Closing game window...")
                        board.cleanup()
                        running = False
                        break
                        
                    print("event.type: ", event.type)
                    print("pygame.MOUSEBUTTONUP: ", pygame.MOUSEBUTTONUP)
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
                                        print("here rewind")
                                        replay_state = replay_handler(idx, currentstuff[0], replay_state, currentstuff[1])
                                        break
                                    if idx == 1: # play button
                                        print("here play")
                                        play_loop = 0
                                        play = True
                                        play_length = len(currentstuff[0])
                                        counter = time.time()
                                        break

                                    if idx == 2: # fast forward
                                        print("here fast forward")
                                        replay_state = replay_handler(idx  , currentstuff[0], replay_state, currentstuff[1])
                                        break
                                    if idx == 3: # exit replay button
                                        print("here exit replay")
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
                                    if idx == 24:
                                        currentstuff = set_replay(idx)
                                        replay = True
                                        break
                                    if removepos == True:
                                                board_positions_now = board.get_positions()
                                                if board.form_mill(idx):
                                                    board.check_remove_active_mill()
                                                    removepos = False
                                                    board.save_current_state_to_log()
                                                    break
                                                break
                                    if board.get_remaining_turns() != 0:
                                        print("here2")
                                        print(f"Clicked on position: {idx}")
                                        if board.place_piece(idx):
                                            board.check_remove_active_mill()
                                            if board.form_mill_GUI():
                                                removepos = True
                                                break
                                            board.save_current_state_to_log()
                                            break
                                    if board.get_remaining_turns() == 0:
                                            if board.is_game_over():
                                                print("Game over!")
                                                print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!")
                                                gameover = True
                                                break
                                            if startpos == None:
                                                startpos = idx
                                                print("startpos: ", startpos)
                                                break
                                            else:
                                                if startpos == idx:
                                                    break
                                                endpos = idx
                                                print("endpos: ", endpos)
                                                if board.player_piece_count() == 3:
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
            if play == True:
                for event in pygame.event.get():
                    print(f"Event: {event}")  # This will print out each event captured
                    if event.type == pygame.QUIT:
                        print("Quit event detected. Closing game window...")
                        board.cleanup()
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
                board.set_positions(state['positions'])
                board.set_player_turn(state['player_turn'])
                board.set_active_mills(state['active_mills'])
                board.set_remaining_turns(state['remaining_turns'])
                board.set_permissible_moves(state['permissible_moves'])
                if pause == True:
                    play_loop = pause_play_loop
                if pause == False:
                    play_loop = round( time.time() - counter )

            #print("startpos: ", startpos)
            #print("endpos: ", endpos)
            # print("removepos: ", removepos)
            # print("replay: ", replay)
            # print("play: ", play)
            # print("board positions: ", board.get_positions())
            # print("board player turn: ", board.get_player_turn())
            #     # Add more event handling logic here for other phases
            # print("remaining turns: ", board.get_remaining_turns())
            # Drawing the game state
            #print("Calling draw_board()...")
            screen.fill(WHITE)
            draw_board(screen, boardImg, board.get_positions(), coords, replay, play)
            if sleep == True:
                time.sleep(1)
                sleep = False
            
            #print("Calling draw_game_info()...")
            draw_game_info(screen, board, gameover)

            # Updating the display
            #print("Updating display...")
            pygame.display.flip()

            # Frame rate
            clock.tick(60)
        except Exception as e:
            print(f"Error in game loop: {e}")
            running = False

    print("Exiting game...")
    # remove temp file
    board.cleanup()

    pygame.quit()
    sys.exit()


game_loop()
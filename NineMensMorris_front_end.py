import sys

import pygame

from backend.NineMensMorris_version7 import Board as Board
from backend.NineMensMorris_version7 import Game_Functions as Game_Functions

# Global Variables
board = Board()
game_functions = Game_Functions()
pygame.font.init()  # you have to call this at the start, 
                    # if you want to use this module.
myfont = pygame.font.SysFont('Arial', 18)
# Print the positions, player turn, active mills, remaining turns, and permissible moves
print("Positions:", board.get_positions())
print("Player Turn:", board.get_player_turn())
print("Active Mills:", board.get_active_mills())
print("Remaining Turns:", board.get_remaining_turns())
print("Permissible Moves:", board.get_permissible_moves())

# Initialize pygame
print(" calling pygame.init()")
pygame.init()
print("pygame initialized")
# Set the size of the screen
screen = pygame.display.set_mode((600, 750))

pygame.display.set_caption("Nine Men Morris")
print("game window initialized")
# nine mens morris board image 
boardImg = pygame.image.load('images/morrisbig.png') 
# avatar images
leafImg = pygame.image.load('images/player1_30x30.png')
fireImg = pygame.image.load('images/player2_30x30.png')
highImg = pygame.image.load('images/high.png')
roboImg = pygame.image.load('images/robo1.png')
# coordinates of each board position in Board and corresponding position in the nine mens morris board image
print("images loaded")
coords = {
    0: (22, 22, 120, 770),
    1: (230, 22, 820, 770),
    2: (450, 22, 230, 660),
    3: (22, 240, 710, 660),
    4: (450, 240, 350, 540),
    5: (22, 450, 590, 540),
    6: (230, 450, 120, 425),
    7: (450, 450, 230, 425),
    8: (95, 95, 350, 425),
    9: (230, 95, 590, 425),
    10: (380, 95, 710, 425),
    11: (95, 240, 820, 425),
    12: (380, 240, 350, 310),
    13: (95, 378, 470, 310),
    14: (230, 378, 590, 310),
    15: (380, 378, 230, 190),
    16: (162, 169, 470, 190),
    17: (230, 169, 710, 190),
    18: (308, 169, 120, 80),
    19: (162, 240, 470, 80),
    20: (308, 240, 820, 80),
    21: (162, 308, 415, 790),
    22: (230, 308, 430, 680),
    23: (308, 308, 430, 575)
}
# coordinates of each clickable position
# mul = 500 / 843
# clickables = [pygame.Rect(mul * c[0], mul * c[1], 35, 35) for c in coords.values()]
clickables = [pygame.Rect(c[0]-20, c[1]-20, 40, 40) for c in coords.values()]
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Functions to draw the game state
def draw_board(screen, board_img, positions, coords):
    try:
        # Draw the background board
        screen.blit(board_img.convert(), (0, 0))

        # Draw the pieces on the board
        for pos, value in enumerate(positions):
            x, y, _, _ = coords[pos]
            if value == 1:
                screen.blit(leafImg.convert_alpha(), (x, y))
            elif value == 2:
                screen.blit(fireImg.convert_alpha(), (x, y))
    except Exception as e:
        print(f"Error drawing the board: {e}")

def draw_game_info(screen, board, gameover):
    # Display the variables from the Board class
    if gameover == True:
        texts = [
        f"Game Over! Player {2 if board.get_player_turn() == 1 else 1} wins!"
    ]
    if gameover == False:    
        texts = [
            f"Positions: {board.get_positions()}",
            f"Player Turn: {board.get_player_turn()}",
            f"Active Mills: {board.get_active_mills()}",
            f"Remaining Turns: {board.get_remaining_turns()}",
        ]

    for i, text in enumerate(texts):
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface, (10, 600 + i*30))

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
    while running:
        try:
            # Event handling
            
            for event in pygame.event.get():
                print(f"Event: {event}")  # This will print out each event captured
                if event.type == pygame.QUIT:
                    print("Quit event detected. Closing game window...")
                    running = False
                    break
                    
                print("event.type: ", event.type)
                print("pygame.MOUSEBUTTONUP: ", pygame.MOUSEBUTTONUP)
                if event.type == pygame.MOUSEBUTTONUP:
                    # Check if a clickable area was clicked
                    print("here")
                    for idx, rect in enumerate(clickables):
                        print("the clickables are: ", enumerate(clickables))
                        print("The idx is: ", idx)
                        print("The rect is: ", rect)
                        print("here1")
                        print("event.pos: ", event.pos)
                        if rect.collidepoint(event.pos):
                            print("here1.5")
                            if removepos == True:
                                        game_functions.form_mill(idx)
                                        game_functions.check_remove_active_mill()
                                        board_info = game_functions.set_board_for_gui()                                    
                                        board.set_active_mills(board_info[2])
                                        removepos = False
                                        game_functions.save_current_state_to_log()
                                        board_info = game_functions.set_board_for_gui()                                    
                                        board.set_player_turn(board_info[1])
                                        board.set_remaining_turns(board_info[3])
                                        break
                            if board.get_remaining_turns() != 0:
                                print("here2")
                                print(f"Clicked on position: {idx}")
                                if game_functions.place_piece(idx):  
                                    game_functions.check_remove_active_mill()
                                    if game_functions.form_mill_GUI():
                                        removepos = True
                                        break
                                    game_functions.save_current_state_to_log()
                                    board_info = game_functions.set_board_for_gui()                                    
                                    board.set_positions(board_info[0])
                                    board.set_remaining_turns(board_info[3])                                    
                                    board.set_player_turn(board_info[1])
                                    break                    
                            if board.get_remaining_turns() == 0:
                                    if game_functions.is_game_over():
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
                                        if game_functions.player_piece_count() == 3:
                                            if game_functions.fly_piece(startpos, endpos):
                                                game_functions.check_remove_active_mill()
                                                if game_functions.form_mill_GUI():
                                                    removepos = True
                                                    break                                                
                                                game_functions.save_current_state_to_log()
                                                board_info = game_functions.set_board_for_gui()                                    
                                                board.set_positions(board_info[0])
                                                board.set_active_mills(board_info[2])
                                                board.set_player_turn(board_info[1])
                                                startpos = None
                                                endpos = None
                                                break                    
                                            else:
                                                startpos = None
                                                endpos = None
                                        else:
                                            if game_functions.move_piece(startpos, endpos):
                                                game_functions.check_remove_active_mill()
                                                if game_functions.form_mill_GUI():
                                                    removepos = True
                                                    break                                               
                                                game_functions.save_current_state_to_log()
                                                board_info = game_functions.set_board_for_gui()                                    
                                                board.set_positions(board_info[0])
                                                board.set_active_mills(board_info[2])
                                                board.set_player_turn(board_info[1])
                                                startpos = None
                                                endpos = None
                                                break 
                                            else:
                                                startpos = None
                                                endpos = None

            print("startpos: ", startpos)
            print("endpos: ", endpos)
            print("removepos: ", removepos)
            print("board positions: ", board.get_positions())
            print("board player turn: ", board.get_player_turn())            
                # Add more event handling logic here for other phases
            print("remaining turns: ", board.get_remaining_turns())
            # Drawing the game state
            print("Calling draw_board()...")
            screen.fill(WHITE)
            draw_board(screen, boardImg, board.get_positions(), coords)
            
            print("Calling draw_game_info()...")
            draw_game_info(screen, board, gameover)

            # Updating the display
            print("Updating display...")
            pygame.display.flip()

            # Frame rate
            clock.tick(60)
        except Exception as e:
            print(f"Error in game loop: {e}")
            running = False

    print("Exiting game...")
    pygame.quit()
    sys.exit()

# #set positions in board to 1 or 2
# board.set_positions([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
#                      2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0])
# # Call the main game loop
#game_functions.new_restart_game()
game_loop()
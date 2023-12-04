import os
import pickle
import sys
import time
import pygame
from NineMensMorris_Game import Game
from NineMensMorris_Board import Board

# Global Variables

# DEBUG - purposes for DEBUGGING
DEBUG = True
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)



# Initialize pygame
pygame.init()
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


class GUI_State():
    def __init__(self):
        # all game state data members
        self.board = Game
        self.coords = {}
        self.is_load = False
        self.is_in_game_mode_selection = False
        self.is_in_sleep = False
        self.is_in_play = False
        self.is_in_replay = False
        self.is_paused = False
        self.is_gameover = False
        self.can_removepiece = False
        # all other data members
        self.startpos = -1
        self.endpos = -1
        self.play_length = -1
        self.boardImg = pygame.Surface
        self.counter = 0
        self.current_log = []

        # replay state and play_loop
        self.replay_state = -1
        self.play_loop = -1

        self.replay_coords = {}
        self.play_coords = {}
        self.selection_coords = {}

        self.selection_clickables = []
        self.play_clickables = []
        self.replay_clickables = [] 
        self.clickables = []
    

     # Setters
    
    def set_clickables(self, clickables: list):
        self.clickables = clickables
    
    def set_selection_clickables(self, selection_clickables: list):
        self.selection_clickables = selection_clickables
    def set_play_clickables(self, play_clickables: list):
        self.play_clickables = play_clickables
    def set_replay_clickables(self, replay_clickables: list):
        self.replay_clickables = replay_clickables
    def set_selection_coords(self, selection_coords: dict):
        self.selection_coords = selection_coords
    def set_play_coords(self, play_coords: dict):
        self.play_coords = play_coords
    def set_replay_coords(self, replay_coords: dict):
        self.replay_coords = replay_coords
    
    def set_board(self, board: Game):
        self.board = board

    def set_coords(self, coords: dict):
        self.coords = coords

    def set_is_load(self, is_load: bool):
        self.is_load = is_load

    def set_is_in_game_mode_selection(self, is_in_game_mode_selection: bool):
        self.is_in_game_mode_selection = is_in_game_mode_selection

    def set_is_in_sleep(self, is_in_sleep: bool):
        self.is_in_sleep = is_in_sleep
    
    def set_is_in_play(self, is_in_play: bool):
        self.is_in_play = is_in_play
    
    def set_is_in_replay(self, is_in_replay: bool):
        self.is_in_replay = is_in_replay
    
    def set_is_paused(self, is_paused: bool):
        self.is_paused = is_paused

    def set_is_gameover(self, is_gameover: bool):
        self.is_gameover = is_gameover

    def set_can_removepiece(self, can_removepiece: bool):
        self.can_removepiece = can_removepiece

    def set_startpos(self, startpos: int):
        self.startpos = startpos

    def set_endpos(self, endpos: int):
        self.endpos = endpos

    def set_play_length(self, play_length: int):
        self.play_length = play_length

    def set_boardImg(self):
        if(self.get_board().get_board_size() == 3):
            self.boardImg = boardImg3
        elif(self.get_board().get_board_size() == 6):
            self.boardImg = boardImg6
        elif(self.get_board().get_board_size() == 9):
            self.boardImg = boardImg9
        else:
            raise Exception("Incorrect board size. Board image could not be set")
    def set_counter(self, counter: int):
        self.counter = counter
    def set_current_log(self, current_log: list):
        self.current_log = current_log
    def set_replay_state(self, replay_state: int):
        self.replay_state = replay_state
    def set_play_loop(self, play_loop: int):
        self.play_loop = play_loop

    # Getters
    def get_clickables(self):
        return self.clickables
    def get_selection_clickables(self):
        return self.selection_clickables
    def get_play_clickables(self):
        return self.play_clickables
    def get_replay_clickables(self):
        return self.replay_clickables
    def get_selection_coords(self):
        return self.selection_coords
    def get_play_coords(self):
        return self.play_coords
    def get_replay_coords(self):
        return self.replay_coords
    
    def get_coords(self):
        return self.coords
    
    def get_board(self):
        return self.board

    def get_is_load(self):
        return self.is_load

    def get_is_in_game_mode_selection(self):
        return self.is_in_game_mode_selection

    def get_is_in_sleep(self):
        return self.is_in_sleep

    def get_is_in_play(self):
        return self.is_in_play

    def get_is_in_replay(self):
        return self.is_in_replay

    def get_is_paused(self):
        return self.is_paused

    def get_is_gameover(self):
        return self.is_gameover

    def get_can_removepiece(self):
        return self.can_removepiece
    
    def get_startpos(self):
        return self.startpos

    def get_endpos(self):
        return self.endpos

    def get_play_length(self):
        return self.play_length

    def get_boardImg(self):
        return self.boardImg

    def get_counter(self):
        return self.counter

    def get_current_log(self):
        return self.current_log

    def get_replay_state(self):
        return self.replay_state

    def get_play_loop(self):
        return self.play_loop 

    # DEBUG LOOP VARIABLES
    def print_loop_variable_statuses(self):
        yes = "yes"
        no = "no"
        print(f"Is In Load Mode: {yes if self.get_is_load() else no}")
        print(f"Is In Game Selection Mode: {yes if self.get_is_in_game_mode_selection() else no}")
        print(f"Is In Sleep: {yes if self.get_is_in_sleep() else no}")
        print(f"Is In Play (within Replay Mode): {yes if self.get_is_in_play() else no}")
        print(f"Is In Replay Mode: {yes if self.get_is_in_replay() else no}")
        print(f"Is In Pause Mode: {yes if self.get_is_paused() else no}")
        print(f"Is Gameover?: {yes if self.get_is_gameover() else no}")
        print(f"Can remove a piece?: {yes if self.get_can_removepiece() else no}")
        print(f"Start position (move/fly phase): {self.get_startpos()}")
        print(f"End position (move/fly phase): {self.get_endpos()}")
        print(f"Play length (replay phase): {self.get_play_length()}")
        print(f"Counter (replay phase): {self.get_counter()}")
        print(f"Replay State (replay phase): {self.get_replay_state()}")
        print(f"Play loop (replay phase): {self.get_play_loop()}")



    def setupLoadGame(self):
        variable_load = ""
        # Check if the load_game.txt file exists and create it if it doesn't
        load_file_path = "load_game.txt"
        if not os.path.exists(load_file_path):
            with open(load_file_path, "w+") as variable_load_file:
                variable_load_file.write('False')

        # Read data from load_game.txt
        with open(load_file_path, "r") as variable_load_file:
            variable_load = variable_load_file.read()
    
        if(variable_load == 'True'):
            self.set_is_load(True)
        elif(variable_load == 'False'):
            self.set_is_load(False)
        else:
            raise Exception("Something went wrong with setting up load game functionality")
    
    def setupCoordsForReplayPlaySelectionClickables(self):
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
        self.set_replay_coords(replay_coords)
        self.set_play_coords(play_coords)
        self.set_selection_coords(selection_coords)

        # DEBUG
        #print("Replay Coords: ", self.get_replay_coords())
        #print("Play Coords: ", self.get_play_coords())
        #print("Selection Coords: ", self.get_selection_coords())


        self.set_replay_clickables([pygame.Rect(c[0], c[1], 30, 30) for c in self.get_replay_coords().values()])
        self.set_play_clickables([pygame.Rect(c[0], c[1], 30, 30) for c in self.get_play_coords().values()])
        self.set_selection_clickables([pygame.Rect(c[0], c[1], 30, 30) for c in self.get_selection_coords().values()])

        # DEBUG
        #print("Replay Clickables: ", self.get_replay_clickables())
        #print("Play Clickables: ", self.get_play_clickables())
        #print("Selection Clickables: ", self.get_selection_clickables())


        

    def setupCoordsForClickables(self):
        if(self.get_board().get_board_size() == 9):
            self.set_coords({
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
            })
        elif(self.get_board().get_board_size() == 6):
            self.set_coords({
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
            })
        elif(self.get_board().get_board_size() == 3):
            self.set_coords({
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
            })
        else:
            raise Exception("Something went wrong when establishing coordinates for clickables")
        self.set_clickables([pygame.Rect(c[0], c[1], 30, 30) for c in self.get_coords().values()])
        #print("Clickables: ", self.get_clickables())

    # DEBUG Making sure board is being set properly inside the class
    def printBoardProperties(self):
        print(f"Board Size: {self.get_board().get_board_size()}")
        print(f"Positions: {self.get_board().get_positions()}")
        print(f"Player Turn: {self.get_board().get_player_turn()}")
        print(f"Remaining Turns: {self.get_board().get_remaining_turns()}")
        print(f"Permissible Moves: {self.get_board().get_permissible_moves()}")
        if(self.get_board().get_game_mode() == 0):
            print(f"Game Mode: Human v Human")
        else:
            print(f"Game Mode: Human v Computer")



        
    def get_replay_restart_btn_coords(self):
        if self.get_board().get_board_size() == 3:
            return self.get_coords()[9], self.get_coords()[10], self.get_coords()[11], self.get_coords()[12]
        elif self.get_board().get_board_size() == 6:
            return self.get_coords()[16], self.get_coords()[17], self.get_coords()[18], self.get_coords()[19]
        elif self.get_board().get_board_size() == 9:
            return self.get_coords()[24], self.get_coords()[25], self.get_coords()[26], self.get_coords()[27]
    
    # Functions to draw the game state
    def draw_board(self):
        try:
            # Draw the background board
            screen.blit(self.get_boardImg().convert(), (0, 0))

            # Draw borders around the clickable areas
            if DEBUG and not (self.get_is_in_replay() and self.get_is_in_play()):
                clickables_to_draw = self.get_replay_clickables() if self.get_is_in_replay() else self.get_clickables()
                for rect in clickables_to_draw:
                    pygame.draw.rect(screen, BLACK, rect, 1)

            # Draw the pieces on the board
            for pos, value in enumerate(self.get_board().get_positions()):
                x, y = self.get_coords()[pos]
                piece_img = None
                if value == 1:
                    piece_img = pantherimg.convert_alpha()
                    screen.blit(piece_img, (x, y))
                elif value == 2:
                    piece_img = dragonimg.convert_alpha()
                    screen.blit(piece_img, (x, y))

            # Highlight selected piece with a green rectangle
            if self.get_startpos() > -1:
                x, y = self.get_coords()[self.get_startpos()]
                pygame.draw.rect(screen, GREEN, (x, y, 30, 30), 3)

            # Draw the selection buttons for game mode
            if self.get_is_in_game_mode_selection():
                screen.blit(single_player.convert_alpha(), (self.get_selection_coords()[1]))
                screen.blit(multi_player.convert_alpha(), (self.get_selection_coords()[2]))

            # Draw replay and other buttons based on the game state
            self.draw_buttons()
        except Exception as e:
            print(f"Error drawing the board: {e}")
    
    def draw_buttons(self):
        replay_button_coord = None
        save_button_coord = None
        load_button_coord = None
        restart_button_coord = None

        if not (self.get_is_in_replay and self.get_is_in_play()):
            replay_button_coord, save_button_coord, load_button_coord, restart_button_coord = self.get_replay_restart_btn_coords()

            screen.blit(replay_button.convert_alpha(), replay_button_coord)
            screen.blit(save_button.convert_alpha(), save_button_coord)
            screen.blit(load_button.convert_alpha(), load_button_coord)
            screen.blit(restart_button.convert_alpha(), restart_button_coord)

        elif self.get_is_in_replay() and not self.get_is_in_play():
            rewind_button_coord, play_button_coord, fast_forward_button_coord, back_button_coord = self.get_replay_coords()[1:]

            screen.blit(rewind_button.convert_alpha(), rewind_button_coord)
            screen.blit(play_button.convert_alpha(), play_button_coord)
            screen.blit(fast_forward_button.convert_alpha(), fast_forward_button_coord)
            screen.blit(back_button.convert_alpha(), back_button_coord)

        elif self.get_is_in_replay and self.get_is_in_play():
            play_button_coord, pause_button_coord, back_button_coord = self.get_play_coords()[1:]

            screen.blit(play_button.convert_alpha(), play_button_coord)
            screen.blit(pause_button.convert_alpha(), pause_button_coord)
            screen.blit(back_button.convert_alpha(), back_button_coord)
    
    def draw_game_info(self):
        texts = []
        gridlocked = self.get_board().is_gridlocked()
        if self.get_is_gameover():
            if self.get_is_in_replay():
                texts = ["In Replay Mode"]
            elif gridlocked:
                texts = [
                    f"Player {1 if self.get_board().get_player_turn() == 1 else 2} is gridlocked! Player {2 if self.get_board().get_player_turn() == 2 else 1} wins!",
                    "Close window to change game settings or click Restart"
                ]
            else:
                texts = [
                    f"Game Over! Player {1 if self.get_board().get_player_turn() == 1 else 2} wins!",
                    "Close window to change game settings or click Restart"
                ]
        elif not self.get_is_gameover() and not self.get_is_in_game_mode_selection():
            if self.get_board().get_remaining_turns() != 0:
                if self.get_can_removepiece():
                    texts = [
                        f"Player {1 if self.get_board().get_player_turn() == 1 else 2} formed a mill!",
                        "Select an opponent's piece to remove from the board."
                    ]
                elif self.get_is_in_replay():
                    texts = ["In Replay Mode"]
                else:
                    texts = [
                        f"It's Player {1 if self.get_board().get_player_turn() == 1 else 2}'s turn!",
                        f"Remaining Turns: {self.get_board().get_remaining_turns()}"
                    ]
            elif self.get_board().get_remaining_turns() == 0:
                if self.get_can_removepiece():
                    texts = [
                        f"Player {1 if self.get_board().get_player_turn() == 1 else 2} formed a mill!",
                        "Select an opponent's piece to remove from the board."
                    ]
                elif self.get_is_in_replay():
                    texts = ["In Replay Mode"]
                else:
                    texts = [
                        f"It's Player {1 if self.get_board().get_player_turn() == 1 else 2}'s turn!",
                        "It's time to move pieces! Select a piece to move then select the position you want to move to."
                    ]
        elif self.get_is_in_game_mode_selection():
            texts = ["Select Game Mode"]

        for i, text in enumerate(texts):
            textsurface = myfont.render(text, False, BLACK)
            screen.blit(textsurface, (10, 600 + i * 30))

    def handle_mouse_up_events(self, 
                               event):
        try:
            if self.get_is_in_replay():
                print("Game is in replay mode")
                for i, rect in enumerate(self.get_replay_clickables()):
                    if rect.collidepoint(event.pos):
                        self.handle_replay_click(i)
                        break
            else:
                print("Game is commencing...")
                for i, rect in enumerate(self.get_clickables()):
                    if rect.collidepoint(event.pos):
                        print("Player clicked on the board...")
                        self.handle_main_game_click(i)
                        break
        except Exception as e:
            print(f"Error handling mouse up events: {e}")


    def handle_side_btn_click(self, clicked_pos):
        if self.get_board().get_board_size() == 9:
            if clicked_pos == 24:
                self.set_current_log(self.get_board().get_current_state_log())
                self.set_is_in_replay(True)
            elif(clicked_pos == 25):
                self.get_board().save()
            elif(clicked_pos == 26):
                self.get_board().load()
            elif(clicked_pos == 27):
                self.get_board().new_restart_game()
                self.set_is_gameover(False)
            else:
                print("Did not click side buttons")
        elif(self.get_board().get_board_size() == 6):
            if(clicked_pos == 16):
                self.set_current_log(self.get_board().get_current_state_log())
                self.set_is_in_replay(True)
            elif(clicked_pos == 17):
                self.get_board().save()
            elif(clicked_pos == 18):
                self.get_board().load()
            elif(clicked_pos == 19):
                self.get_board().new_restart_game()
                self.set_is_gameover(False)
            else:
                print("Did not click side buttons")
        elif(self.get_board().get_board_size() == 3):
            if(clicked_pos == 9):
                self.set_current_log(self.get_board().get_current_state_log())
                self.set_is_in_replay(True)
            elif(clicked_pos == 10):
                self.get_board().save()
            elif(clicked_pos == 11):
                self.get_board().load()
            elif(clicked_pos == 12):
                self.get_board().new_restart_game()
                self.set_is_gameover(False)
            else:
                print("Did not click side buttons")
        else:
            raise Exception("Incorrect board size. Something went wrong")
    
    def handle_remove_piece(self, clicked_pos):
        # if a piece can be removed
        if self.get_can_removepiece():
            # check if a mill was formed
            if self.get_board().form_mill(clicked_pos):
                # check if a moved or flown piece was from a previously formed mill
                self.get_board().check_remove_active_mill()
                # set check if a piece can be removed to false
                self.set_can_removepiece(False)
                # save current state to the log and switches the turn
                self.get_board().save_current_state_to_log()
                # check if the game is over or gridlocked (This gameover check only happens in 6 mens or 9 mens morris)
                if (self.get_board().is_game_over() or self.get_board().is_gridlocked()) and (self.get_board().get_board_size() == 6 or self.get_board().get_board_size() == 9) and self.get_board().get_remaining_turns() == 0:
                    self.set_is_gameover(True)
        # if no piece can be removed, just save to log
        else:
            self.get_board().save_current_state_to_log()
            print("Can't remove a piece")

        
    def handle_main_game_click(self, clicked_pos):
        try:
            # Handle main game clicks based on the index
            # DEBUG print(f"Main game click: {index}")
            # Add logic here
            # result is the current log, whether or not the game is in replay mode, and whether the game is over
            self.handle_side_btn_click(clicked_pos)
            # Placing pieces phase
            if self.get_board().get_remaining_turns() != 0:
                # player places a piece on the board
                if self.get_board().place_piece(clicked_pos):
                    # check if a moved or flown piece was from a previously formed mill
                    self.get_board().check_remove_active_mill()
                    # check if a mill was formed in the GUI, removepiece is set to true if 9 mens or 6 mens
                    if self.get_board().form_mill_GUI() and (self.get_board().get_board_size() == 6 or self.get_board().get_board_size() == 9):
                        self.set_can_removepiece(True)
                    # check if a mill was formed in the GUI, save state to log and it is gameover for 3 mens
                    elif self.get_board().form_mill_GUI() and self.get_board().get_board_size() == 3:
                        self.get_board().save_current_state_to_log()
                        self.set_is_gameover(True)
                    #else:
                        #print("Mill was not formed by this piece placement")
                    self.handle_remove_piece(clicked_pos)
            # Move/Fly piece phase
            elif self.get_board().get_remaining_turns() == 0:
                # check if the game is over or gridlocked, if so, game is over
                if self.get_board().is_game_over() or self.get_board().is_gridlocked():
                    self.set_is_gameover(True)

                # grab current position of player AND... 
                if self.get_startpos() == -1:
                    self.set_startpos(clicked_pos)
                    print(f"Start position: ", self.get_startpos())
                    print(f"End position (before click): ", self.get_endpos())
                    return
                # grab the end position of the player
                if self.get_endpos() == -1:
                    self.set_endpos(clicked_pos)
                    print(f"End position: ", self.get_endpos())
            
                # start of fly piece logic (you can only fly pieces in 9 mens or 6 mens)
                if self.get_board().player_piece_count() == 3 and (self.get_board().get_board_size() == 6 or self.get_board().get_board_size() == 9):
                    # player flies a piece
                    if self.get_board().fly_piece(self.get_startpos(), self.get_endpos()):
                        # check if a flown piece was from a previously formed mill
                        self.get_board().check_remove_active_mill()
                        # check if a mill was formed in the GUI
                        if self.get_board().form_mill_GUI():
                            # set the check if a piece can be removed to true
                            self.set_can_removepiece(True)
                    else:
                        # reset current position of piece flown and end position of piece flown
                        self.set_startpos(-1)
                        self.set_endpos(-1)
                        return
                # start of move piece logic
                else:
                    if self.get_board().move_piece(self.get_startpos(), self.get_endpos()):
                        # check if a moved piece was from a previously formed mill
                        self.get_board().check_remove_active_mill()
                        # check if a mill was formed in the GUI and if it is 6 mens or 9 mens
                        if self.get_board().form_mill_GUI() and (self.get_board().get_board_size() == 6 or self.get_board().get_board_size() == 9):
                            # set the check if a piece can be removed to true
                            self.set_can_removepiece(True)
                        # check if a mill was formed in the GUI and if it is 3 mens
                        if self.get_board().form_mill_GUI() and self.get_board().get_board_size() == 3:
                            # save the current state to the log and switch turn
                            self.get_board().save_current_state_to_log()
                            # the game is over
                            self.set_is_gameover(True)
                    else:
                        # reset current position of piece moved and end position of piece moved
                        self.set_startpos(-1)
                        self.set_endpos(-1)
                        return
                
                self.handle_remove_piece(clicked_pos)
                # reset current position of piece flown and end position of piece flown
                self.set_startpos(-1)
                self.set_endpos(-1)
        except Exception as e:
            print(f"Error handling main game click: {e}")
    
    def handle_computer_turn(self):
        if self.get_board().get_remaining_turns() != 0:
            self.get_board().computer_place_piece()
            if self.get_board().form_mill_GUI() and (self.get_board().get_board_size() == 6 or self.get_board().get_board_size() == 9):
                self.set_can_removepiece(True)
                remove_piece = self.get_board().computer_remove_piece()
            elif self.get_board().form_mill_GUI() and self.get_board().get_board_size() == 3:
                self.set_is_gameover(True)
            if self.get_can_removepiece():
                if self.get_board().form_mill(remove_piece):
                    self.set_can_removepiece(False)
                    self.get_board().check_remove_active_mill()
        
        elif(self.get_board().get_remaining_turns() == 0):
            if self.get_board().player_piece_count() != 3:
                self.get_board().computer_move_piece()
            elif self.get_board().player_piece_count() == 3 and (self.get_board().get_board_size() == 6 or self.get_board().get_board_size() == 9):
                self.get_board().computer_fly_piece() 
                if self.get_board().form_mill_GUI() and (self.get_board().get_board_size() == 6 or self.get_board().get_board_size() == 9):
                    self.set_can_removepiece(True)
                    remove_piece = self.get_board().computer_remove_piece()
                if self.get_board().form_mill_GUI() and self.get_board().get_board_size() == 3:
                    self.set_is_gameover(True)
                if self.get_can_removepiece(True):
                    if self.get_board().form_mill(remove_piece):
                        self.set_can_removepiece(False)
                        self.get_board().check_remove_active_mill()
        self.get_board().save_current_state_to_log()


    def handle_replay_click(self, clicked_pos):
        if clicked_pos:
            print("In replay mode")
    '''
    replay_playload = None
    try:
        # Handle replay clicks based on the index and current state
        # DEBUG print(f"Replay click: {index}")
        if len(current_log) > 0:
            if clicked_pos == 0: # rewind a move button
                replay_state = replay_handler(clicked_pos, current_log[0], replay_state, current_log[1])
            elif clicked_pos == 1: # play button
                play_loop = 0
                play = True
                play_length = len(current_log[0])
                counter = time.time()
            elif clicked_pos == 2: # fast forward
                replay_state = replay_handler(clicked_pos, current_log[0], replay_state, current_log[1])
            elif clicked_pos == 3: # exit replay button
                replay_state = replay_handler(clicked_pos, current_log[0],  replay_state, current_log[1])
                replay = False
        else:
            raise Exception("Current log is empty")
    except Exception as e:
        print(f"Error handling replay click: {e}")
    replay_playload = [replay, play_loop, play, play_length, counter]
    return replay_playload
    '''


    def game_loop(self):
        # DEBUG print("Initializing game window")
        screen.fill(WHITE)
        clock = pygame.time.Clock()
        running = True
        #print("Entering game loop....")

        while running:
            try:
                # Event handling
                if not self.get_is_in_game_mode_selection():
                    if not self.get_is_in_play():
                        for event in pygame.event.get():
                            # DEBUG print(f"Event: {event}")
                            if event.type == pygame.QUIT:
                                # DEBUG print("Quit event detected. Closing game window...")
                                running = False
                                break
                            elif event.type == pygame.MOUSEBUTTONUP:
                                self.handle_mouse_up_events(event)
                    elif self.get_is_in_play():
                        print("Game is in replay play mode")
                        #self.handle_play_events(event)
                elif self.get_is_in_game_mode_selection():
                    print("Game is in game mode selection")
                    #self.handle_game_mode_selection(pygame.event.get())
                
                if self.get_board().get_player_turn() == 2 and self.get_board().get_game_mode() == 1:
                    print("Game is in computer turn mode")
                    self.handle_computer_turn()

                screen.fill(WHITE)
                self.set_boardImg()
                self.draw_board()
                if self.get_is_in_sleep():
                    time.sleep(1)
                    self.set_is_in_sleep(False)
                self.draw_game_info()
                pygame.display.flip()
                clock.tick(60)
            except Exception as e:
                print(f"Error in game loop: {e}")
                running = False
        

def setupBoard():
    board = Game()
    # Set up the new board
    board_size = 0
    computer = 0
    # Extract board size from the system (from the previous screen)
    if len(sys.argv) > 1:
        board_size_comm = sys.argv[1]
        board_size = int(board_size_comm[0])
        computer = int(board_size_comm[1])
    # Set up the board
    board.set_board_size(board_size)
    board.set_initial_positions()
    board.set_player_turn(1)
    board.set_initial_remaining_turns()
    board.set_initial_permissible_moves()
    board.set_game_mode(computer)
    return board



def main():
    gamestate = GUI_State()
    gamestate.set_board(setupBoard())
    gamestate.setupCoordsForClickables()
    gamestate.setupCoordsForReplayPlaySelectionClickables()
    gamestate.game_loop()


main()













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
'''
def game_loop(is_loaded):

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



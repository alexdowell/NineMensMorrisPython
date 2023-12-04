import copy
import os
import pickle
import random
from NineMensMorris_Board import Board

class Game(Board):
    TEMP_LOG_PATH = "temp_log.pkl"
    SAVED_LOG_PATH = "board_log.pkl"
    def __init__(self):
        # calling super class's constructor
        super().__init__()
        # Add this new member for the in-memory log
        self.__temp_log = []
        
        # check if log exists or create an empty one
        if not os.path.exists("board_log.pkl"):
            with open("board_log.pkl", "wb") as file:
                pickle.dump([], file)

    # checks if a position is occupied on the board and returns a boolean
    def is_occupied(self, position):
        return self.get_positions()[position] != 0
    
    # checks if the position is occupied by the CURRENT PLAYER (This will be used in move_piece and fly_piece methods)
    def is_current_player(self, position):
        return self.get_positions()[position] == self.get_player_turn()

    # counts how many of each player's pieces is on the board
    def count_current_player_positions(self):
        return self.get_positions().count(self.get_player_turn())

    # helps the player place a piece on the board. Depending on the board size, the upper limit (or the last position to place piece) changes
    def place_piece(self, position):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        elif(self.get_board_size() == 3):
            upper_limit = 8
        # the position needs to be within the limits of the board
        if 0 <= position <= upper_limit:
            # the posiiton where the player is going to place a piece needs to be unoccupied
            if not self.is_occupied(position):
                self.get_positions()[position] = self.get_player_turn()
                self.set_remaining_turns(self.get_remaining_turns() - 1)
            return True
        else:
            return False
    # helps the player move a piece on the board. Depending on the board size, the upper limit (or the last position to move a piece changes)
    def move_piece(self, current_position, move_to):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        elif(self.get_board_size() == 3):
            upper_limit = 8
    
        #print("Upper limit: ", upper_limit)
        if 0 <= current_position <= upper_limit and 0 <= move_to <= upper_limit:
            # 1) the current position (the piece the player will move) needs to be occupied
            # 2) the piece needs to be the player's piece
            # 3) the position that they move to needs to be a move that is permissible (can't be invalid)
            # 4) the position that they move the piece needs to be unoccupied
            if self.is_occupied(current_position) and self.is_current_player(current_position) and self.is_permissible(current_position, move_to) and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                print("piece moved")
                return True
        else:
            print("piece not moved")
            return False
    # checks if the move piece/fly piece action is valid (where the position where the player moved the piece is a permissible move)
    def is_permissible(self, current_position, move_to):
        return move_to in self.get_permissible_moves()[current_position]
    # helps player remove a piece from the board (This method is only used when the board size is 9 or 6)
    def remove_piece(self, position):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        
        if 0 <= position <= upper_limit:
            # the piece that the player removes cannot be their own piece and the position they remove it from has to be occupied
            if self.is_occupied(position) and not self.is_current_player(position):
                self.get_positions()[position] = 0
                print("piece removed")
                return True
        else:
            return False
    # helps the player fly a piece on the board (This method is only used when the board size is 9 or 6)
    def fly_piece(self, current_position, move_to):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        
        if 0 <= current_position <= upper_limit and 0 <= move_to <= upper_limit:
            # 1) the current position they fly from needs to be occupied and has to be their piece
            # 2) the position they fly to can't be occupied
            if self.is_occupied(current_position) and self.is_current_player(current_position) and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                return True
        else:
            return False
    # method that checks if a mill was formed after placing, moving, or flying a piece
    # depending on the board the mill_combinations will change
    '''
    Note:
    There are two methods called "form_mill" in the backend. 
    One is used to make actual changes in the backend 
    and the other is just a check to see if the mill is formed on the frontend.

    '''
    def form_mill(self, position):
        mill_combinations = []
        if(self.get_board_size() == 3):
            mill_combinations = [
            [0, 1, 2], [0, 4, 8], [0, 3, 6],
            [1, 4, 7], [2, 4, 6], [2, 5, 8],
            [6, 7, 8]
            ]
        elif(self.get_board_size() == 6):
            mill_combinations = [
            [0, 1, 2], [0, 6, 13], [2, 9, 15],
            [3, 4, 5], [3, 7, 10], [5, 8, 12],
            [10, 11, 12], [13, 14, 15]
            ]
        elif(self.get_board_size() == 9):
            mill_combinations = [
            [0, 1, 2], [2, 4, 7], [5, 6, 7],
            [0, 3, 5], [8, 9, 10], [10, 12, 15],
            [13, 14, 15], [8, 11, 13],
            [16, 17, 18], [18, 20, 23], [21, 22, 23],
            [16, 19, 21], [1, 9, 17], [20, 12, 4],
            [22, 14, 6], [3, 11, 19]
            ]
        # keep track of newly formed mills
        newly_formed_mills = []
        for combo in mill_combinations:
            # check if pieces form a mill based on the mill combinations 
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                # if the mill formed hasn't been set as an active mill, add it to the newly formed mills list
                if combo not in self.get_active_mills():
                    newly_formed_mills.append(combo)
        # if a new mill is formed by the current player, the current player can then remove a piece and then that newly formed mill is added to the active mills
        # Note: Players can remove pieces only in 6 men's morris or 9 men's morris
        if newly_formed_mills and (self.get_board_size() == 6 or self.get_board_size() == 9):
            # DEBUG print("positions before removing piece:", self.get_positions())
            if self.remove_piece(position):
                # DEBUG print("positions after removing piece:", self.get_positions())
                self.set_active_mills(self.get_active_mills() + newly_formed_mills)
                return True
        # if a new mill is formed and the game is 3 men's morris, it adds the newly formed mill to the active mills
        elif newly_formed_mills and self.get_board_size() == 3:
            self.set_active_mills(self.get_active_mills() + newly_formed_mills)

    def form_mill_GUI(self):
        mill_combinations = None
        if(self.get_board_size() == 3):
            mill_combinations = [
            [0, 1, 2], [0, 4, 8], [0, 3, 6],
            [1, 4, 7], [2, 4, 6], [2, 5, 8],
            [6, 7, 8], [3, 4, 5]
            ]
        elif(self.get_board_size() == 6):
            mill_combinations = [
            [0, 1, 2], [0, 6, 13], [2, 9, 15],
            [3, 4, 5], [3, 7, 10], [5, 8, 12],
            [10, 11, 12], [13, 14, 15]
            ]
        elif(self.get_board_size() == 9):
            mill_combinations = [
            [0, 1, 2], [2, 4, 7], [5, 6, 7],
            [0, 3, 5], [8, 9, 10], [10, 12, 15],
            [13, 14, 15], [8, 11, 13],
            [16, 17, 18], [18, 20, 23], [21, 22, 23],
            [16, 19, 21], [1, 9, 17], [20, 12, 4],
            [22, 14, 6], [3, 11, 19]
            ]
        # DEBUG print("Board size: ", self.get_board_size())

        # keep track of newly formed mills
        newly_formed_mills = []
        # DEBUG print("backend positions:", self.get_positions())
        # DEBUG print("backend player turn:", self.get_player_turn())
        for combo in mill_combinations:
            # DEBUG print(" ==== Comparison ====")
            # DEBUG print(self.get_positions()[combo[0]], "," ,self.get_positions()[combo[1]], "," , self.get_positions()[combo[2]])
            # check if pieces form a mill based on the mill combinations 
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                # DEBUG print("combo:", combo)
                # if the mill formed hasn't been set as an active mill, add it to the newly formed mills list
                if combo not in self.get_active_mills():
                    # DEBUG print("newly formed mill:", combo)
                    newly_formed_mills.append(combo)
                    return True 
        return False
    # method that lets the computer place a piece after the human player makes a turn
    def opposite_player_turn(self):
        if not self.get_player_turn() == 1:
            self.computer_place_piece()

    # method that checks if a player moved or flown a piece that in a mill
    def check_remove_active_mill(self):
        mills_to_remove = []

        for mill in self.get_active_mills():
            player_at_mill = self.get_positions()[mill[0]]
            # when a player moves a piece from a mill, add it to the mills that need to be removed from active mills
            if not (self.get_positions()[mill[0]] == self.get_positions()[mill[1]] == self.get_positions()[mill[2]] == player_at_mill):
                mills_to_remove.append(mill)

        for mill in mills_to_remove:
            # remove the active mill that the player broke
            self.get_active_mills().remove(mill)

    # check if the game is over (This method is only called in 6 men's or 9 men's morris)
    # if a player has only 2 pieces left or can't move anywhere else, the game is over
    def is_game_over(self):
        current_player_pieces = self.get_positions().count(self.get_player_turn())
        return current_player_pieces <= 2
    # method that returns the amount of the current player's pieces on the board
    def player_piece_count(self):
        return self.get_positions().count(self.get_player_turn())
    # method that returns if the player is gridlocked (where player cannot move anywhere)
    def is_gridlocked(self):
        opponent = 2 if self.get_player_turn() == 1 else 1
        for position, player in enumerate(self.get_positions()):
            if player == opponent:
                permissible = self.get_permissible_moves()[position]
                if any([self.get_positions()[move] == 0 for move in permissible]):
                    return False
        # DEBUG print(f"Player {opponent} is gridlocked and Player {self.get_player_turn()} wins!")
        return True
    # method to select a position to move for the computer player (it always picks a random position)
    def computer_move_to(self,move_from): #picks a spot to move to
        permissible_moves = self.get_permissible_moves()[move_from]
        empty_positions = [pos for pos in permissible_moves if self.is_occupied(pos) == False]
        return random.choice(empty_positions)

    # method to select a piece to move/piece to fly for the computer player (it always picks a random piece)
    def computer_select_piece(self): #picks a spot to move from
        player2_positions = [pos for pos, player in enumerate(self.get_positions()) if player == 2]
        choice = True
        while choice == True:
            ranchoice = random.choice(player2_positions)
            # select a permissible move list in the persmissible_moves dictionary with the key of ranchoice
            permissible_move = self.get_permissible_moves()[ranchoice]

            for position in permissible_move:
                if self.is_occupied(position) == False:
                    choice = False

        return ranchoice
    # method to select a position to fly to for the computer player (it always picks a random position)
    def computer_fly_to(self): #picks a spot to move to
        # pick a random position that is not occupied
        empty_positions = [pos for pos, player in enumerate(self.get_positions()) if player == 0]
        return random.choice(empty_positions)
    
    # method to fly the piece for the computer player
    def computer_fly_piece(self):
        current_position = self.computer_select_piece()
        move_to = self.computer_fly_to()
        self.fly_piece(current_position, move_to)
        # DEBUG print(f"Computer flew a piece from {current_position} to {move_to}")

    # method to place a piece for the computer player
    def computer_place_piece(self):
        position = self.computer_fly_to()
        self.place_piece(position)
        print("Computer placed a piece at position", position)
    # method to move a piece for the computer player
    def computer_move_piece(self):
        current_position = self.computer_select_piece()
        move_to = self.computer_move_to(current_position)
        print("move from: ", current_position)
        print("move to: ", move_to)
        print("positions: ", self.get_positions())
        self.move_piece(current_position, move_to)
    # method to remove a piece for the computer player (always removes a random piece from the opposing player)
    def computer_remove_piece(self):
        player1_positions = [pos for pos, player in enumerate(self.get_positions()) if player == 1]
        ranchoice = random.choice(player1_positions)
        return ranchoice
    # method to control the place piece and move/fly pieces for computer player
    def computer_turn_actions(self):
        if self.get_remaining_turns() > 0:
            self.computer_place_piece()
        else:
            self.computer_move_piece()
    # Saves the current state of the game to the temp log
    def save_current_state_to_log(self):
        state = {
            'board_size': self.get_board_size(),
            'positions': copy.deepcopy(self.get_positions()),
            'player_turn': self.get_player_turn(),
            'active_mills': copy.deepcopy(self.get_active_mills()),
            'remaining_turns': self.get_remaining_turns(),
            'permissible_moves': self.get_permissible_moves(),
        }
        # DEBUG print("State before appending to temp_log:", state)  # Debug statement
        self.__temp_log.append(state)
        # DEBUG print("all states in temp_log:", self.__temp_log)  # Debug statement
        self.persist_log('temp')  # Persist to temporary log
        self.set_player_turn(2 if self.get_player_turn() == 1 else 1)


    # Keeps the temp log active in case it disappears during the game
    def persist_log(self, log_type):
        filepath = self.TEMP_LOG_PATH if log_type == 'temp' else self.SAVED_LOG_PATH
        with open(filepath, "wb") as file:
            pickle.dump(self.__temp_log, file)
        print(f"Saved {len(self.__temp_log)} logs to {filepath}")  # Debug statement

    # method to save a game (this saves the current state of the game to a file)
    def save(self):
        # Print all states in the temp_log before saving
        print("States in log before saving:")
        for index, s in enumerate(self.__temp_log, 1):
            print(f"State {index}:")
            print(s)
            print("----------")
        
        # Clear the saved log and then save the current temporary log
        if os.path.exists(self.SAVED_LOG_PATH):
            os.remove(self.SAVED_LOG_PATH)
        self.persist_log('saved')
        print("Board state saved to saved log.")
    # method to load a game (this takes the previously saved file from the file system and loads it into the game)
    def load(self):
        if not os.path.exists(self.SAVED_LOG_PATH):
            print("No saved game state exists.")
            return

        with open(self.SAVED_LOG_PATH, "rb") as file:
            self.__temp_log = pickle.load(file)

        if not self.__temp_log:  # Check if the list is empty
            print("Saved log is empty.")
            return

        state = self.__temp_log[-1]  # Now it's safe to access the last element
    
        self.set_board_size(state['board_size'])
        self.set_positions(state['positions'])
        self.set_player_turn(state['player_turn'])
        self.set_active_mills(state['active_mills'])
        self.set_remaining_turns(state['remaining_turns'])
        self.set_permissible_moves(state['permissible_moves'])

        # DEBUG self.printBoard()
        print("Board state loaded from log.")
        # DEBUG self.play_game()  # This will continue the game from the loaded state.
    # method to restart a game
    def new_restart_game(self):
        self.set_board_size(self.get_board_size())
        self.set_initial_positions()
        self.set_player_turn(1)
        self.set_active_mills([])
        self.set_initial_remaining_turns()
        self.set_initial_permissible_moves()
        if os.path.exists(self.TEMP_LOG_PATH):
            os.remove(self.TEMP_LOG_PATH)
        self.__temp_log = []  # clear the in-memory log
    
    def get_current_state_log(self):
        print("replay function called")
        if not os.path.exists(self.TEMP_LOG_PATH):
            print("No saved game states to replay.")
            return
        with open(self.TEMP_LOG_PATH, "rb") as file:
            log = pickle.load(file)
        if not log:
            print("Log is empty. Nothing to replay.")
            return
        # Save current state
        current_state = {
            'board_size': self.get_board_size(),
            'positions': self.get_positions(),
            'player_turn': self.get_player_turn(),
            'active_mills': self.get_active_mills(),
            'remaining_turns': self.get_remaining_turns(),
            'permissible_moves': self.get_permissible_moves(),
            'game_mode': self.get_game_mode()
        }
        current_log = [log,current_state]
        return current_log
    
    def change_replay_state(self, state):
        self.set_board_size(state['board_size'])
        self.set_board_size(state['board_size'])
        self.set_positions(state['positions'])
        self.set_player_turn(state['player_turn'])
        self.set_active_mills(state['active_mills'])
        self.set_remaining_turns(state['remaining_turns'])
        self.set_game_mode(state['game_mode'])


    def replay_handler(self, replay_option, replay_state):
        current_state_log = self.get_current_state_log()
        log = current_state_log[0]
        current_state = current_state_log[1]
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
            state = log[replay_state]
            self.change_replay_state(state)
            return replay_state
        elif replay_option == 2:
            if index != (len(log)-1): # fast forward button
                index += 1
                replay_state = index
            else:
                index = 0
                replay_state = index
        # DEBUG print("log length: ", len(log))
        # DEBUG print("index: ", index)
            state = log[replay_state]
            self.change_replay_state(state)
            return replay_state
        if replay_option == 3: # exit replay button
            #reset current state
            self.change_replay_state(current_state)
            return



        

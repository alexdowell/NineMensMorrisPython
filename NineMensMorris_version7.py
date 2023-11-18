import atexit
import copy
import os
import pickle
import signal
import sys
import time


class Board:
    def __init__(self):
        self.__board_size = None
        self.__positions = []
        self.__player_turn = 1
        self.__active_mills = []
        self.__remaining_turns = 0
        self.__permissible_moves = {}
    # Setter for board size
    def set_board_size(self, board_size):
        self.__board_size = board_size
            
    # Getter for board size
    def get_board_size(self):
        return self.__board_size

    # Getter for positions
    def get_positions(self):
        return self.__positions
    
    # Setter for different positions
    def set_positions_diff(self):
        if(self.get_board_size() == 3):
            self.__positions = [0] * 9
        elif(self.get_board_size() == 6):
            self.__positions = [0] * 16
        elif(self.get_board_size() == 9):
            self.__positions = [0] * 24
    # Setter for positions
    def set_positions(self, positions):
        self.__positions = positions

    # Getter for player_turn
    def get_player_turn(self):
        return self.__player_turn

    # Setter for player_turn
    def set_player_turn(self, player_turn):
        self.__player_turn = player_turn

    # Getter for active_mills
    def get_active_mills(self):
        return self.__active_mills

    # Setter for active_mills
    def set_active_mills(self, active_mills):
        self.__active_mills = active_mills

    # Getter for remaining_turns
    def get_remaining_turns(self):
        return self.__remaining_turns
    
    # Setter for different remaining turns
    def set_remaining_turns_diff(self):
        if(self.get_board_size() == 3):
            self.__remaining_turns = 6
        elif(self.get_board_size() == 6):
            self.__remaining_turns = 12
        elif(self.get_board_size() == 9):
            self.__remaining_turns = 18

    # Setter for remaining_turns
    def set_remaining_turns(self, remaining_turns):
        self.__remaining_turns = remaining_turns

    # Getter for permissible_moves
    def get_permissible_moves(self):
        return self.__permissible_moves
    
    # Setter for different remaining turns
    def set_permissible_moves_diff(self):
        if(self.get_board_size() == 3):
            self.__permissible_moves = {
                0: [1, 3, 4],
                1: [0, 2, 4],
                2: [1, 4, 5],
                3: [0, 4, 6],
                4: [0, 1, 2, 3, 4, 5, 6, 7, 8],
                5: [2, 4, 8],
                6: [3, 4, 7],
                7: [4, 6, 8],
                8: [4, 5, 7]
            }
        elif(self.get_board_size() == 6):
            self.__permissible_moves = {
                0: [1, 6],
                1: [0, 2, 4],
                2: [1, 9],
                3: [4, 7],
                4: [1, 3, 5],
                5: [4, 8],
                6: [0, 7, 13],
                7: [3, 6, 10],
                8: [5, 9, 12],
                9: [2, 8, 15],
                10: [7, 11],
                11: [10, 12, 14],
                12: [8, 11],
                13: [6, 14],
                14: [11, 13, 15],
                15: [9, 14]
            }
        elif(self.get_board_size() == 9):
            self.__permissible_moves = {
                0: [1, 3],
                1: [0, 2, 9],
                2: [1, 4],
                3: [0, 11, 5],
                4: [2, 12, 7],
                5: [3, 6],
                6: [5, 7, 14],
                7: [4, 6],
                8: [9, 11],
                9: [1, 8, 17, 10],
                10: [9, 12],
                11: [8, 3, 19, 13],
                12: [20, 10, 4, 15],
                13: [11, 14],
                14: [13, 22, 6, 15],
                15: [14, 12],
                16: [19, 17],
                17: [16, 18, 9],
                18: [17, 20],
                19: [16, 11, 21],
                20: [18, 12, 23],
                21: [19, 22],
                22: [14, 21, 23],
                23: [20, 22]
            }
    
    # Setter for permissible moves
    def set_permissible_moves(self, permissible_moves):
        self.__permissible_moves = permissible_moves

class Game_Functions(Board):
    TEMP_LOG_PATH = "temp_log.pkl"
    SAVED_LOG_PATH = "board_log.pkl"
    def __init__(self):
        super().__init__()
        # Add this new member for the in-memory log
        self.__temp_log = []

        # Handle exit events
        #atexit.register(self.cleanup)
        #signal.signal(signal.SIGINT, self.signal_handler)
        
        # check if log exists or create an empty one
        if not os.path.exists("board_log.pkl"):
            with open("board_log.pkl", "wb") as file:
                pickle.dump([], file)

    def is_occupied(self, position):
        return self.get_positions()[position] != 0

    def is_current_player(self, position):
        return self.get_positions()[position] == self.get_player_turn()

    def count_current_player_positions(self):
        return self.get_positions().count(self.get_player_turn())


    def place_piece(self, position):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        elif(self.get_board_size() == 3):
            upper_limit = 8
    
        if 0 <= position <= upper_limit:
            if not self.is_occupied(position):
                self.get_positions()[position] = self.get_player_turn()
                self.set_remaining_turns(self.get_remaining_turns() - 1)
                return True
        else:
            return False

    def move_piece(self, current_position, move_to):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        elif(self.get_board_size() == 3):
            upper_limit = 8
    
        if 0 <= current_position <= upper_limit and 0 <= move_to <= upper_limit:
            if self.is_occupied(current_position) and self.is_current_player(current_position) and move_to in self.get_permissible_moves()[current_position] and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                return True
        else:
            return False

    def is_permissible(self, current_position, move_to):
        return move_to in self.get_permissible_moves()[current_position]

    def remove_piece(self, position):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        
        if 0 <= position <= upper_limit:
            if self.is_occupied(position) and not self.is_current_player(position):
                self.get_positions()[position] = 0
                print("piece removed")
                return True
        else:
            return False

    def fly_piece(self, current_position, move_to):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = 23
        elif(self.get_board_size() == 6):
            upper_limit = 15
        
        if 0 <= current_position <= upper_limit and 0 <= move_to <= upper_limit:
            if self.is_occupied(current_position) and self.is_current_player(current_position) and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                return True
        else:
            return False
    
    def form_mill_diff(self, position):
        mill_combinations = []
        if(self.get_board_size() == 3):
            mill_combinations = [
            [0, 1, 2], [0, 4, 8], [0, 3, 6],
            [1, 4, 7], [2, 4, 6], [2, 5, 8],
            [6, 7, 8]
            ]
        elif(self.get_board_size == 6):
            mill_combinations = [
            [0, 1, 2], [0, 6, 13], [2, 9, 15],
            [3, 4, 5], [3, 7, 10], [5, 8, 12],
            [10, 11, 12], [13, 14, 15]
            ]
        elif(self.get_board_size == 9):
            mill_combinations = [
            [0, 1, 2], [2, 4, 7], [5, 6, 7],
            [0, 3, 5], [8, 9, 10], [10, 12, 15],
            [13, 14, 15], [8, 11, 13],
            [16, 17, 18], [18, 20, 23], [21, 22, 23],
            [16, 19, 21], [1, 9, 17], [20, 12, 4],
            [22, 14, 6], [3, 11, 19]
            ]
        
        newly_formed_mills = []
        for combo in mill_combinations:
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                if combo not in self.get_active_mills():
                    newly_formed_mills.append(combo)
        if newly_formed_mills and (self.get_board_size() == 6 or self.get_board_size() == 9):
            self.set_active_mills(self.get_active_mills() + newly_formed_mills)
            self.remove_piece(position)
        elif newly_formed_mills and self.get_board_size() == 3:
            self.set_active_mills(self.get_active_mills() + newly_formed_mills)
            self.is_game_over_diff()

    def form_mill(self, position):
        mill_combinations = [
        [0, 1, 2], [2, 4, 7], [5, 6, 7],
        [0, 3, 5], [8, 9, 10], [10, 12, 15],
        [13, 14, 15], [8, 11, 13],
        [16, 17, 18], [18, 20, 23], [21, 22, 23],
        [16, 19, 21], [1, 9, 17], [20, 12, 4],
        [22, 14, 6], [3, 11, 19]
        ]
        newly_formed_mills = []

        for combo in mill_combinations:
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                if combo not in self.get_active_mills():
                    newly_formed_mills.append(combo)

        if newly_formed_mills:
            if self.remove_piece(position):
                self.set_active_mills(self.get_active_mills() + newly_formed_mills)
                return True

    def form_mill_GUI(self):
        mill_combinations = []
        if(self.get_board_size() == 3):
            mill_combinations = [
            [0, 1, 2], [0, 4, 8], [0, 3, 6],
            [1, 4, 7], [2, 4, 6], [2, 5, 8],
            [6, 7, 8]
            ]
        elif(self.get_board_size == 6):
            mill_combinations = [
            [0, 1, 2], [0, 6, 13], [2, 9, 15],
            [3, 4, 5], [3, 7, 10], [5, 8, 12],
            [10, 11, 12], [13, 14, 15]
            ]
        elif(self.get_board_size == 9):
            mill_combinations = [
            [0, 1, 2], [2, 4, 7], [5, 6, 7],
            [0, 3, 5], [8, 9, 10], [10, 12, 15],
            [13, 14, 15], [8, 11, 13],
            [16, 17, 18], [18, 20, 23], [21, 22, 23],
            [16, 19, 21], [1, 9, 17], [20, 12, 4],
            [22, 14, 6], [3, 11, 19]
            ]
        newly_formed_mills = []
        print("backend positions:", self.get_positions())
        print("backend player turn:", self.get_player_turn())
        for combo in mill_combinations:
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                print("combo:", combo)
                if combo not in self.get_active_mills():
                    print("newly formed mill:", combo)
                    newly_formed_mills.append(combo)
                    return True

    def opposite_player_turn(self):
        if self.get_player_turn() == 1:
            return 2
        else:
            return 1

    def check_remove_active_mill(self):
        mills_to_remove = []

        for mill in self.get_active_mills():
            player_at_mill = self.get_positions()[mill[0]]
            if not (self.get_positions()[mill[0]] == self.get_positions()[mill[1]] == self.get_positions()[mill[2]] == player_at_mill):
                mills_to_remove.append(mill)

        for mill in mills_to_remove:
            self.get_active_mills().remove(mill)
    
    def is_game_over_diff(self):
        if(self.get_board_size() == 6 or self.get_board_size() == 9):
            current_player_pieces = self.get_positions().count(self.get_player_turn())
            return current_player_pieces <= 2
        elif(self.get_board_size() == 3):
            return self.get_active_mills()[0][0] == self.get_player_turn() and self.get_active_mills()[0][1] == self.get_player_turn() and self.get_active_mills()[0][2] == self.get_player_turn()


    def is_game_over(self):
        current_player_pieces = self.get_positions().count(self.get_player_turn())
        return current_player_pieces <= 2

    def player_piece_count(self):
        return self.get_positions().count(self.get_player_turn())

    def is_gridlocked(self):
        opponent = 2 if self.get_player_turn() == 1 else 1
        for position, player in enumerate(self.get_positions()):
            if player == opponent:
                permissible = self.get_permissible_moves()[position]
                if any([self.get_positions()[move] == 0 for move in permissible]):
                    return False
        print(f"Player {opponent} is gridlocked and Player {self.get_player_turn()} wins!")
        exit()

    def start_menu(self):
        choice = input("Select: 1. New/Restart Game 2. Load Game 3. Game Type (default is 9): ")
        if choice == '1':
            self.new_restart_game()
        elif choice == '2':
            self.load()
        elif choice == '3':
            print("Currently, only Nine Men's Morris (9) is supported.")
            self.new_restart_game()
        else:
            print("Invalid choice.")
            self.start_menu()

    def save_current_state_to_log(self):
        state = {
            'positions': copy.deepcopy(self.get_positions()),
            'player_turn': self.get_player_turn(),
            'active_mills': copy.deepcopy(self.get_active_mills()),
            'remaining_turns': self.get_remaining_turns(),
            'permissible_moves': self.get_permissible_moves()
        }
        print("State before appending to temp_log:", state)  # Debug statement
        self.__temp_log.append(state)
        print("all states in temp_log:", self.__temp_log)  # Debug statement
        self.persist_log('temp')  # Persist to temporary log
        self.set_player_turn(2 if self.get_player_turn() == 1 else 1)



    def persist_log(self, log_type):
        filepath = self.TEMP_LOG_PATH if log_type == 'temp' else self.SAVED_LOG_PATH
        with open(filepath, "wb") as file:
            pickle.dump(self.__temp_log, file)
        print(f"Saved {len(self.__temp_log)} logs to {filepath}")  # Debug statement


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

        self.set_positions(state['positions'])
        self.set_player_turn(state['player_turn'])
        self.set_active_mills(state['active_mills'])
        self.set_remaining_turns(state['remaining_turns'])
        self.set_permissible_moves(state['permissible_moves'])

        #self.printBoard()
        print("Board state loaded from log.")
        #self.play_game()  # This will continue the game from the loaded state.
    
    def new_restart_game(self):
        self.set_positions([0] * 24)
        self.set_player_turn(1)
        self.set_active_mills([])
        self.set_remaining_turns(18)
        os.remove(self.TEMP_LOG_PATH)
        self.__temp_log = []  # clear the in-memory log

'''
def new_restart_game(self):
    self.set_positions([0] * 24)
    self.set_player_turn(1)
    self.set_active_mills([])
    self.set_remaining_turns(18)
    if os.path.exists(self.TEMP_LOG_PATH):
        os.remove(self.TEMP_LOG_PATH)
    self.__temp_log = []  # clear the in-memory log

    def cleanup(self):
        if os.path.exists(self.TEMP_LOG_PATH):
            print("\nGame exited, temporary log cleared.")
            os.remove(self.TEMP_LOG_PATH)

    def signal_handler(self, signal, frame):
        self.cleanup()
        sys.exit(0)

def main():
    game = Game_Functions()  # Create a Game_Functions object.
    game.start_menu()  # Start the game with the main menu.

if __name__ == "__main__":
    main()
'''

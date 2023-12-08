import pickle
import os
import random
import copy
from NineMensMorris_Board import Board

class Game(Board):
    TEMP_LOG_PATH = "temp_log.pkl"
    SAVED_LOG_PATH = "board_log.pkl"
    NINE_MENS_MILL_COMBOS = [
            [0, 1, 2], [2, 4, 7], [5, 6, 7],
            [0, 3, 5], [8, 9, 10], [10, 12, 15],
            [13, 14, 15], [8, 11, 13],
            [16, 17, 18], [18, 20, 23], [21, 22, 23],
            [16, 19, 21], [1, 9, 17], [20, 12, 4],
            [22, 14, 6], [3, 11, 19]
    ]
    SIX_MENS_MILL_COMBOS = [
            [0, 1, 2], [0, 6, 13], [2, 9, 15],
            [3, 4, 5], [3, 7, 10], [5, 8, 12],
            [10, 11, 12], [13, 14, 15]
    ]
    THREE_MENS_MILL_COMBOS = [
            [0, 1, 2], [0, 4, 8], [0, 3, 6],
            [1, 4, 7], [2, 4, 6], [2, 5, 8],
            [6, 7, 8]
    ]

    NINE_MENS_LAST_POSITION = 23
    SIX_MENS_LAST_POSITION = 15
    THREE_MENS_LAST_POSITION = 8


    def __init__(self):
        super().__init__()
        # Add this new member for the in-memory log
        self.__temp_log = []
        # self.computer_player = ComputerPlayer(self)


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
            upper_limit = self.NINE_MENS_LAST_POSITION
        elif(self.get_board_size() == 6):
            upper_limit = self.SIX_MENS_LAST_POSITION
        elif(self.get_board_size() == 3):
            upper_limit = self.THREE_MENS_LAST_POSITION
    
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
            upper_limit = self.NINE_MENS_LAST_POSITION
        elif(self.get_board_size() == 6):
            upper_limit = self.SIX_MENS_LAST_POSITION
        elif(self.get_board_size() == 3):
            upper_limit = self.THREE_MENS_LAST_POSITION
    
        print("Upper limit: ", upper_limit)
        if 0 <= current_position <= upper_limit and 0 <= move_to <= upper_limit:
            if self.is_occupied(current_position) and self.is_current_player(current_position) and move_to in self.get_permissible_moves()[current_position] and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                print("piece moved")
                return True
        else:
            print("piece not moved")
            return False

    def is_permissible(self, current_position, move_to):
        return move_to in self.get_permissible_moves()[current_position]
    


    def remove_piece(self, position):
        upper_limit = 0
        if(self.get_board_size() == 9):
            upper_limit = self.NINE_MENS_LAST_POSITION
        elif(self.get_board_size() == 6):
            upper_limit = self.SIX_MENS_LAST_POSITION
        
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
            upper_limit = self.NINE_MENS_LAST_POSITION
        elif(self.get_board_size() == 6):
            upper_limit = self.SIX_MENS_LAST_POSITION
        
        if 0 <= current_position <= upper_limit and 0 <= move_to <= upper_limit:
            if self.is_occupied(current_position) and self.is_current_player(current_position) and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                return True
        else:
            return False
    
    def form_mill(self, position):
        mill_combinations = []
        if(self.get_board_size() == 3):
            mill_combinations = self.THREE_MENS_MILL_COMBOS
        elif(self.get_board_size() == 6):
            mill_combinations = self.SIX_MENS_MILL_COMBOS
        elif(self.get_board_size() == 9):
            mill_combinations = self.NINE_MENS_MILL_COMBOS
        
        newly_formed_mills = []
        for combo in mill_combinations:
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                if combo not in self.get_active_mills():
                    newly_formed_mills.append(combo)
        if newly_formed_mills and (self.get_board_size() == 6 or self.get_board_size() == 9):
            print("positions before removing piece:", self.get_positions())
            if self.remove_piece(position):
                print("positions after removing piece:", self.get_positions())
                self.set_active_mills(self.get_active_mills() + newly_formed_mills)
                return True
        elif newly_formed_mills and self.get_board_size() == 3:
            self.set_active_mills(self.get_active_mills() + newly_formed_mills)

    def form_mill_GUI(self):
        mill_combinations = None
        if(self.get_board_size() == 3):
            mill_combinations = self.THREE_MENS_MILL_COMBOS
        elif(self.get_board_size() == 6):
            mill_combinations = self.SIX_MENS_MILL_COMBOS
        elif(self.get_board_size() == 9):
            mill_combinations = self.NINE_MENS_MILL_COMBOS
        #print("Board size: ", self.get_board_size())
        newly_formed_mills = []
        #print("backend positions:", self.get_positions())
        #print("backend player turn:", self.get_player_turn())
        for combo in mill_combinations:
            #print(" ==== Comparison ====")
            print(self.get_positions()[combo[0]], "," ,self.get_positions()[combo[1]], "," , self.get_positions()[combo[2]])
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                #print("combo:", combo)
                if combo not in self.get_active_mills():
                    #print("newly formed mill:", combo)
                    newly_formed_mills.append(combo)
                    return True 
        return False

    def check_remove_active_mill(self):
        mills_to_remove = []

        for mill in self.get_active_mills():
            player_at_mill = self.get_positions()[mill[0]]
            if not (self.get_positions()[mill[0]] == self.get_positions()[mill[1]] == self.get_positions()[mill[2]] == player_at_mill):
                mills_to_remove.append(mill)

        for mill in mills_to_remove:
            self.get_active_mills().remove(mill)

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
        #print(f"Player {opponent} is gridlocked and Player {self.get_player_turn()} wins!")
        return True

    def computer_move_from(self):
        positions = self.get_positions()
        computer_positions = [pos for pos, player in enumerate(positions) if player == 2]
        print("computer positions: ", computer_positions)
        mill_combinations = self.mill_list()

        for current_position in computer_positions:
            for move in self.get_permissible_moves()[current_position]:
                if not self.is_occupied(move):
                    # Check for blocking human mills
                    print("about to check for blocking human mills")
                    if self.blocks_opponent_mill(current_position, move, positions, mill_combinations):
                        print("blocking human mill")
                        from_and_to = [current_position, move]
                        return from_and_to
        for current_position in computer_positions:
            print("current position: ", current_position)
            for move in self.get_permissible_moves()[current_position]:
                print("permissible_moves: ", self.get_permissible_moves()[current_position])
                if not self.is_occupied(move):
                    # Check for forming computer mills
                    print("about to check for forming computer mill")
                    if self.forms_own_new_mill(current_position, move, positions, mill_combinations):
                        print("forming computer mill")
                        from_and_to = [current_position, move]
                        return from_and_to
        for current_position in computer_positions:
            print("current position: ", current_position)
            for move in self.get_permissible_moves()[current_position]:
                print("permissible_moves: ", self.get_permissible_moves()[current_position])
                if not self.is_occupied(move):
                    # Check for forming computer mills
                    print("about to check for un forming computer mill for next turn")
                    if self.un_form_computer_mill(current_position, positions):
                        print("un forming computer mill")
                        from_and_to = [current_position, move]
                        return from_and_to
        for current_position in computer_positions:
            for move in self.get_permissible_moves()[current_position]:
                if not self.is_occupied(move):
                    # Check for creating two-in-a-row
                    print("about to check for two in a row")
                    if self.creates_two_in_a_row(current_position, move, positions, mill_combinations):
                        print("creating two in a row")
                        from_and_to = [current_position, move]
                        return from_and_to
        still_thinking = True
        while still_thinking == True:
            choice = random.choice(computer_positions) if computer_positions else None
            for move in self.get_permissible_moves()[choice]:
                if not self.is_occupied(choice):
                    still_thinking = False
        return [choice, move]
            
    def blocks_opponent_mill(self, current_position, new_position, positions, mill_combinations):
        positions[current_position] = 0
        positions[new_position] = 1
        for combo in mill_combinations:
            if all(positions[pos] == 1 for pos in combo) and new_position in combo:
                positions[current_position] = 2
                positions[new_position] = 0
                return True
        positions[current_position] = 2
        positions[new_position] = 0
        return False
    #makes sure that a new mill is formed with the new position
    def forms_own_new_mill(self, current_position, new_position, positions, mill_combinations):
        positions[current_position] = 0
        positions[new_position] = 2
        for combo in mill_combinations:
            if all(positions[pos] == 2 for pos in combo) and new_position in combo:
                positions[current_position] = 2
                positions[new_position] = 0
                return True
        positions[current_position] = 2
        positions[new_position] = 0
        return False

    def un_form_computer_mill(self, current_position, positions):
        # get the current player's active mills
        active_mills = self.get_active_mills()
        computers_active_mills = []
        for mill in active_mills:
            if positions[mill[0]] == positions[mill[1]] == positions[mill[2]] == 2:
                computers_active_mills.append(mill)
        # look and see if current position is in the computers active mills. If it is, then return true, otherwise return false
        for mill in computers_active_mills:
            if current_position in mill:
                return True
        return False


    def creates_two_in_a_row(self, current_position, new_position, positions, mill_combinations):
        positions[current_position] = 0
        positions[new_position] = 2
        for combo in mill_combinations:
            if sum(positions[pos] == 2 for pos in combo) == 2 and any(positions[pos] == 0 for pos in combo):
                positions[current_position] = 2
                positions[new_position] = 0
                return True
        positions[current_position] = 2
        positions[new_position] = 0
        return False
    
    def mill_list(self):
            mill_combinations = []
            if(self.get_board_size() == 3):
                mill_combinations = self.THREE_MENS_MILL_COMBOS
            elif(self.get_board_size() == 6):
                mill_combinations = self.SIX_MENS_MILL_COMBOS
            elif(self.get_board_size() == 9):
                mill_combinations = self.NINE_MENS_MILL_COMBOS
            return mill_combinations
            
    def computer_fly_to(self):
        positions = self.get_positions()  # Get current board positions
        mill_combinations = self.mill_list()  # Get mill combinations based on board size

        # 1. Block human player's potential mill
        for combo in mill_combinations:
            if self.is_two_in_a_row_and_empty(combo, positions, player=1):
                return self.find_empty_in_combo(combo, positions)

        # 2. Form computer's own mill
        for combo in mill_combinations:
            if self.is_two_in_a_row_and_empty(combo, positions, player=2):
                return self.find_empty_in_combo(combo, positions)

        # 3. Move based on mill combinations
        for combo in mill_combinations:
            for position in combo:
                if positions[position] == 2:  # If a computer piece is part of the combo
                    for pos in combo:
                        if positions[pos] == 0:  # If position in combo is empty
                            return pos  # Move here

        # If no move is found, return a random empty position (or handle differently as needed)
        empty_positions = [pos for pos, player in enumerate(positions) if player == 0]
        return random.choice(empty_positions) if empty_positions else None


    def is_two_in_a_row_and_empty(self, combo, positions, player):
        count = sum(positions[pos] == player for pos in combo)
        empty_count = sum(positions[pos] == 0 for pos in combo)
        return count == 2 and empty_count == 1

    def find_empty_in_combo(self, combo, positions):
        for pos in combo:
            if positions[pos] == 0:
                return pos
                if positions[pos] == 0:
                    return pos

    def computer_fly_piece(self):
        from_and_to = self.computer_move_from()
        current_position = from_and_to[0]
        move_to = self.computer_fly_to()
        self.fly_piece(current_position, move_to)
        print(f"Computer flew a piece from {current_position} to {move_to}")


    def computer_place_piece(self):
        position = self.computer_fly_to()
        self.place_piece(position)
        print("Computer placed a piece at position", position)

    def computer_move_piece(self):
        from_and_to = self.computer_move_from()
        print("move from: ", from_and_to[0])
        print("move to: ", from_and_to[1])
        print("positions: ", self.get_positions())
        self.move_piece(from_and_to[0], from_and_to[1])
        return from_and_to

    def computer_remove_piece(self):
        player1_positions = [pos for pos, player in enumerate(self.get_positions()) if player == 1]
        ranchoice = random.choice(player1_positions)
        return ranchoice


    def save_current_state_to_log(self):
        state = {
            'board_size': self.get_board_size(),
            'positions': copy.deepcopy(self.get_positions()),
            'player_turn': self.get_player_turn(),
            'active_mills': copy.deepcopy(self.get_active_mills()),
            'remaining_turns': self.get_remaining_turns(),
            'permissible_moves': self.get_permissible_moves()
        }
        #print("State before appending to temp_log:", state)  # Debug statement
        self.__temp_log.append(state)
        #print("all states in temp_log:", self.__temp_log)  # Debug statement
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
    
        self.set_board_size(state['board_size'])
        self.set_positions(state['positions'])
        self.set_player_turn(state['player_turn'])
        self.set_active_mills(state['active_mills'])
        self.set_remaining_turns(state['remaining_turns'])
        self.set_permissible_moves(state['permissible_moves'])

        #self.printBoard()
        print("Board state loaded from log.")
        #self.play_game()  # This will continue the game from the loaded state.
    
    def new_restart_game(self):
        self.set_board_size(self.get_board_size())
        self.set_initial_positions()
        self.set_player_turn(1)
        self.set_active_mills([])
        self.set_initial_remaining_turns()
        self.set_initial_permissible_moves()
        self.set_game_mode(self.get_game_mode())
        if os.path.exists(self.TEMP_LOG_PATH):
            os.remove(self.TEMP_LOG_PATH)
        self.__temp_log = []  # clear the in-memory log

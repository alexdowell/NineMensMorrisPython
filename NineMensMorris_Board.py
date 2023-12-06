
class Board:
    def __init__(self):
        # data member for game mode (human v human or human v computer)
        self.__game_mode = -1
        # data member for board size
        self.__board_size = 0
        # data member for positions of the board
        self.__positions = []
        # data member for the player turn ('1' for player 1, '2' for player 2)
        # default value is 1
        self.__player_turn = 1
        # data member for keeping track of the active mills on the board
        self.__active_mills = []
        # data member for the total number of pieces per game (total remaining turns of player 1 + player 2)
        # default value is 0
        self.__remaining_turns = 0
        # data member for the permissible moves per positon of the board
        self.__permissible_moves = {}
    # Setter for game mode 
    def set_game_mode(self, mode):
        self.__game_mode = mode
    # Getter for game mode
    def get_game_mode(self):
        return self.__game_mode
    # Setter for board size
    def set_board_size(self, board_size):
        self.__board_size = board_size
            
    # Getter for board size
    def get_board_size(self):
        return self.__board_size

    # Getter for positions
    def get_positions(self):
        return self.__positions
    
    # Setter for initial positions
    def set_initial_positions(self):
        if(self.get_board_size() == 3):
            self.__positions = [0] * 9
        elif(self.get_board_size() == 6):
            self.__positions = [0] * 16
        elif(self.get_board_size() == 9):
            self.__positions = [0] * 24
    
    # Setter for positions (when loading or saving a game)
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
    
    # Setter for initial remaining turns
    def set_initial_remaining_turns(self):
        if(self.get_board_size() == 3):
            self.__remaining_turns = 6
        elif(self.get_board_size() == 6):
            self.__remaining_turns = 12
        elif(self.get_board_size() == 9):
            self.__remaining_turns = 18
    
    # Setter for remaining turns (when loading or saving a game)
    def set_remaining_turns(self, remaining_turns):
        self.__remaining_turns = remaining_turns

    # Getter for permissible_moves
    def get_permissible_moves(self):
        return self.__permissible_moves
    
    # Setter for initial permissible moves
    def set_initial_permissible_moves(self):
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

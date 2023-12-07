# Import necessary libraries/modules
import numbers
import subprocess
import tkinter as tk
from tkinter import messagebox

# Class for displaying game instructions
class GameInstructions:
    def __init__(self):
        # Initialize the Tkinter window for game instructions
        self.window = tk.Tk()
        self.window.title("Game Instructions")
        self.window.geometry("800x600")
        self.window.configure(background="#FFFFCC")

        # Text with game instructions
        instructions_text = """Nine Men's Morris Game Instructions:
        The game proceeds in three phases:
        
        1. Placing men on vacant points.
        2. Moving men to adjacent points.
        3. (Flying phase) Moving men to any vacant point when the player has been reduced to three men.
        
        Game Objective:
        
        - Try to form a mill, so that you can remove the opponent's men.
        - To win, reduce the opponent's men to two.
        - To win, make the opponent make a move.
        
        Have fun playing Nine Men's Morris!
        """

        # Label to display game instructions
        instructions_label = tk.Label(self.window, text=instructions_text, font=("Arial", 16), justify="left")
        instructions_label.pack(pady=20, padx=20, anchor="w")

        # Button to go back
        back_button = tk.Button(self.window, text="Back", font=("Arial", 24), bg="#FFCCCC", command=self.go_back, width=10)
        back_button.pack(pady=10)

    # Method to destroy the window and go back
    def go_back(self):
        self.window.destroy()

    # Method to run the Tkinter main loop
    def run(self):
        self.window.mainloop()

# Class for selecting game modes
class GameModes:
    def __init__(self):
        # Initialize the Tkinter window for game modes
        self.window = tk.Tk()
        self.window.title("Game Modes")
        self.window.geometry("800x600")
        self.window.configure(background="yellow")

        # Set common font size
        self.font_large = ("Arial", 24)

        # Set a common width for all buttons
        self.button_field_width = 15  

        # Create buttons for different game modes
        self.button1 = tk.Button(self.window, text="Human vs Human", font=self.font_large, bg="pink", command=self.human_vs_human, width=self.button_field_width)
        self.button2 = tk.Button(self.window, text="Human vs Computer", font=self.font_large, bg="#CCCCFF", command=self.human_vs_computer, width=self.button_field_width)
        self.button3 = tk.Button(self.window, text="Nine Men's Morris", font=self.font_large, bg="#CCFFCC", command=self.nine_mens_morris, width=self.button_field_width)
        self.board_size_label = tk.Label(self.window, text="Board Size: ", font=self.font_large)
        self.board_size_field = tk.Entry(self.window, font=self.font_large, width=self.button_field_width)
        self.board_size_field.insert(0, "9")
        self.exit_button = tk.Button(self.window, text="Exit", font=self.font_large, bg="red", command=self.window.destroy, width=self.button_field_width)
        self.rules_button = tk.Button(self.window, text="Rules", font=self.font_large, bg="orange", command=self.show_game_instructions, width=self.button_field_width)

        # Pack buttons and labels
        self.button1.pack(pady=10)
        self.button2.pack(pady=10)
        self.button3.pack(pady=10)
        self.board_size_label.pack(pady=10)
        self.board_size_field.pack(pady=10)
        self.rules_button.pack(pady=10)
        self.exit_button.pack(pady=10)

    # Method to start Human vs Human game
    def human_vs_human(self):
        # Get the board size from the entry field
        board_size_comm = self.board_size_field.get() + "0"
        # Check if the input is a valid number and the board size is 3, 6, or 9
        if(isinstance(int(board_size_comm[0]), numbers.Number) and
           (int(board_size_comm[0]) == 3 or int(board_size_comm[0]) == 6 or int(board_size_comm[0]) == 9)):
            # Construct the command to start the game
            command = ['python', 'GUI.py', board_size_comm]
            # Open a subprocess to start the game
            subprocess.Popen(command)
            print("Starting Human vs Human Game")
        else:
            # Reset the board size field and show an error message
            self.board_size_field.delete(0, len(self.board_size_field.get()))
            self.board_size_field.insert(0, "9")
            messagebox.showerror("Error", "Invalid Board Size. Please enter either 3, 6, or 9.")

    # Method to start Human vs Computer game
    def human_vs_computer(self):
        # Get the board size from the entry field
        board_size_comm = self.board_size_field.get() + "1"
        # Check if the input is a valid number and the board size is 3, 6, or 9
        if(isinstance(int(board_size_comm[0]), numbers.Number) and
           (int(board_size_comm[0]) == 3 or int(board_size_comm[0]) == 6 or int(board_size_comm[0]) == 9)):
            # Construct the command to start the game
            command = ['python', 'GUI.py', board_size_comm]
            # Open a subprocess to start the game
            subprocess.Popen(command)
            print("Starting Human vs Computer Game")
        else:
            # Reset the board size field and show an error message
            self.board_size_field.delete(0, len(self.board_size_field.get()))
            self.board_size_field.insert(0, "9")
            messagebox.showerror("Error", "Invalid Board Size. Please enter either 3, 6, or 9.")

    # Method for starting Nine Men's Morris game
    def nine_mens_morris(self):
        print("Starting Nine Men's Morris Game")

    # Method to show game instructions
    def show_game_instructions(self):
        game_instructions = GameInstructions()
        game_instructions.run()

# Class for the start menu
class StartMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Start Menu")
        self.geometry("800x600")
        self.configure(background="#87CEEB")

        title_font = ("Arial", 48, "bold")
        button_font = ("Arial", 18)

        # Create labels and buttons for the start menu
        self.title_label = tk.Label(self, text="Nine Men's Morris", font=title_font)
        self.title_label.pack(pady=20)

        self.new_game_button = tk.Button(self, text="New Game", font=button_font, command=self.show_new_game_options, width=15)
        self.new_game_button.pack(pady=10)

        self.rules_button = tk.Button(self, text="Rules", font=button_font, command=self.show_game_instructions, width=15)
        self.rules_button.pack(pady=10)

        self.load_game_button = tk.Button(self, text="Load Game", font=button_font, command=self.load_game, width=15)
        self.load_game_button.pack(pady=10)

        self.exit_button = tk.Button(self, text="Exit Game", font=button_font, command=self.quit, width=15)
        self.exit_button.pack(pady=10)

    # Method to show game instructions
    def show_game_instructions(self):
        game_instructions = GameInstructions()
        game_instructions.run()

    # Method to show new game options
    def show_new_game_options(self):
        new_game_window = GameModes()

    # Method to load a saved game
    def load_game(self):
        variable_load = open("load_game.txt", "w+")
        variable_load.write('True')

        # Construct the command to start the game
        command = ['python', 'GUI.py']
        # Open a subprocess to start the game
        subprocess.Popen(command)
        print("Starting Human vs Human Game")

# Main block to run the application
if __name__ == "__main__":
    app = StartMenu()
    app.mainloop()
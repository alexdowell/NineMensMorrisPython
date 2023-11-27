import numbers
import subprocess
import tkinter as tk
from tkinter import messagebox
from NineMensMorris_version7 import Game_Functions


class GameInstructions:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game Instructions")
        self.window.geometry("800x600")
        self.window.configure(background="#FFFFCC")

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

        instructions_label = tk.Label(self.window, text=instructions_text, font=("Arial", 16), justify="left")
        instructions_label.pack(pady=20, padx=20, anchor="w")

        back_button = tk.Button(self.window, text="Back", font=("Arial", 24), bg="#FFCCCC", command=self.go_back, width=10)
        back_button.pack(pady=10)

    def go_back(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()

class GameModes:
    def __init__(self):
        self.game = Game_Functions()
        self.window = tk.Tk()
        self.window.title("Game Modes")
        self.window.geometry("800x600")
        self.window.configure(background="yellow")

        self.font_large = ("Arial", 24)

        self.button_field_width = 15  # Set a common width for all buttons

        self.button1 = tk.Button(self.window, text="Human vs Human", font=self.font_large, bg="pink", command=self.human_vs_human, width=self.button_field_width)
        self.button2 = tk.Button(self.window, text="Human vs Computer", font=self.font_large, bg="#CCCCFF", command=self.human_vs_computer, width=self.button_field_width)
        self.button3 = tk.Button(self.window, text="Nine Men's Morris", font=self.font_large, bg="#CCFFCC", command=self.nine_mens_morris, width=self.button_field_width)
        self.board_size_label = tk.Label(self.window, text="Board Size: ", font=self.font_large)
        self.board_size_field = tk.Entry(self.window, font=self.font_large, width=self.button_field_width)
        self.board_size_field.insert(0, "9")
        self.exit_button = tk.Button(self.window, text="Exit", font=self.font_large, bg="red", command=self.window.destroy, width=self.button_field_width)
        self.rules_button = tk.Button(self.window, text="Rules", font=self.font_large, bg="orange", command=self.show_game_instructions, width=self.button_field_width)

        self.button1.pack(pady=10)
        self.button2.pack(pady=10)
        self.button3.pack(pady=10)
        self.board_size_label.pack(pady=10)
        self.board_size_field.pack(pady=10)
        self.rules_button.pack(pady=10)
        self.exit_button.pack(pady=10)

    def human_vs_human(self):
        board_size = self.board_size_field.get()
        if(isinstance(int(board_size), numbers.Number) and
           (int(board_size) == 3 or int(board_size) == 6 or int(board_size) == 9)):
            self.game.set_board_size(int(board_size))
            command = ['python', 'NineMensMorris_front_end_computer.py', board_size]
            subprocess.Popen(command)
            print("Starting Human vs Human Game")
        else:
            self.board_size_field.delete(0, len(self.board_size_field.get()))
            self.board_size_field.insert(0, "9")
            messagebox.showerror("Error", "Invalid Board Size. Please enter either 3, 6, or 9.")


    def human_vs_computer(self):
        board_size = self.board_size_field.get()
        
        if(isinstance(int(board_size), numbers.Number) and
           (int(board_size) == 3 or int(board_size) == 6 or int(board_size) == 9)):
            self.game.set_board_size(int(board_size))
            command = ['python', 'NineMensMorris_front_end_computer.py', board_size]
            subprocess.Popen(command)
            print("Starting Human vs Computer Game")
        else:
            self.board_size_field.delete(0, len(self.board_size_field.get()))
            self.board_size_field.insert(0, "9")
            messagebox.showerror("Error", "Invalid Board Size. Please enter either 3, 6, or 9.")
        
        


    def nine_mens_morris(self):
        print("Starting Nine Men's Morris Game")

    def show_game_instructions(self):
        game_instructions = GameInstructions()
        game_instructions.run()

class StartMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Start Menu")
        self.geometry("800x600")
        self.configure(background="#87CEEB")

        self.game = Game_Functions()

        title_font = ("Arial", 48, "bold")
        button_font = ("Arial", 18)

        self.title_label = tk.Label(self, text="Nine Men's Morris", font=title_font)
        self.title_label.pack(pady=20)

        self.game_functions = Game_Functions() 

        self.new_game_button = tk.Button(self, text="New Game", font=button_font, command=self.show_new_game_options, width=15)
        self.new_game_button.pack(pady=10)

        self.rules_button = tk.Button(self, text="Rules", font=button_font, command=self.show_game_instructions, width=15)
        self.rules_button.pack(pady=10)

        self.load_game_button = tk.Button(self, text="Load Game", font=button_font, command=self.load_game, width=15)
        self.load_game_button.pack(pady=10)

        self.exit_button = tk.Button(self, text="Exit Game", font=button_font, command=self.quit, width=15)
        self.exit_button.pack(pady=10)

    def show_game_instructions(self):
        game_instructions = GameInstructions()
        game_instructions.run()

    def show_new_game_options(self):
        new_game_window = GameModes()

    def load_game(self):
        # self.game_functions.load()
        # open up a boolean data or text file or create one if it doesn't exist and name it load_game.txt

        variable_load = open("load_game.txt", "w+")
        variable_load.write('True')

        command = ['python', 'NineMensMorris_front_end_computer.py']
        subprocess.Popen(command)
        print("Starting Human vs Human Game")

if __name__ == "__main__":
    app = StartMenu()
    app.mainloop()
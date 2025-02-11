# CS5551 - Project
# Nine Men's Morris Game

## Description
This project implements a digital version of the classic board game **Nine Men's Morris** using Python. The game supports different board sizes (3x3, 6x6, and 9x9) and features a GUI-based interface for gameplay. Players can place, move, and remove pieces according to the traditional rules of the game.

## Features
- Supports **3x3**, **6x6**, and **9x9** board sizes.
- Implements **piece placement, movement, and removal** mechanics.
- **Mill detection** for valid three-in-a-row formations.
- **Computer AI** to play against the user.
- **Save and load functionality** for game states.
- **Graphical User Interface (GUI)** for an interactive experience.

## Installation

### Prerequisites
Ensure you have Python installed along with the necessary dependencies:
```sh
pip install -r requirements.txt

## Running the Game
Execute the following command to start the game:

```sh
python NineMensMorris_GUI.py

## File Structure
- **NineMensMorris_GUI.py** → Handles the graphical user interface.
- **NineMensMorris_Board.py** → Manages board state and logic.
- **NineMensMorris_Game.py** → Implements gameplay mechanics and rules.

## Gameplay

### Phase 1: Placing Pieces
- Players take turns placing their 9 pieces on the board.
- If three pieces align, a mill is formed, allowing the player to remove an opponent's piece.

### Phase 2: Moving Pieces
- Once all pieces are placed, players can move their pieces along valid paths.

### Phase 3: Flying (For 3 Pieces Left)
- When a player has only 3 pieces left, they can move to any empty space.

### Winning the Game
- A player wins by reducing the opponent to 2 pieces or by blocking all their moves.

## Controls
- **Left-click** to select a piece.
- **Left-click** on a valid position to move it.
- If a mill is formed, **click** on an opponent's piece to remove it.

## Save & Load
The game supports saving and loading game states using `pickle`:

- **Save**: Automatically stores the latest board state.
- **Load**: Resumes from the last saved game.

## Contributions
Feel free to fork this repository and contribute!

**Authors**: Alexander Dowell, Ashna Ali

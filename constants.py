# Maximum number of rounds in the game
MAX_ROUNDS = 3

# Valid moves in the game
VALID_MOVES = {"rock", "paper", "scissors", "bomb"}

# Moves that beat other moves (excluding bomb)
WIN_RULES = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}

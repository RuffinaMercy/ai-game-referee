import random

from google.adk.agents import Agent

from game_state import GameState
from constants import VALID_MOVES
from game_tools import validate_move, resolve_round, update_game_state
from enums import ValidationStatus


# -------------------------------
# Deterministic Test Configuration
# -------------------------------
# Set to True for reproducible testing
TEST_MODE = True 

# Fixed bot moves when TEST_MODE is enabled
TEST_BOT_MOVES = ["rock", "paper", "scissors"]
# -------------------------------


def explain_rules():
    print(
        "Welcome to Rock–Paper–Scissors–Plus!\n"
        "Rules:\n"
        "1. Best of 3 rounds\n"
        "2. Moves: rock, paper, scissors, bomb\n"
        "3. Bomb beats everything but can be used once\n"
        "4. Invalid input wastes the round\n"
    )


def get_bot_move(state: GameState, user_move: str | None = None) -> str:
    """
    Smarter bot strategy:
    - Save bomb for later rounds
    - Counter repeated user moves
    - Fall back to random choice
    """

    # Deterministic test mode
    if TEST_MODE:
        index = (state.round_number - 1) % len(TEST_BOT_MOVES)
        move = TEST_BOT_MOVES[index]
        if move == "bomb" and state.bot_bomb_used:
            return "rock"
        return move

    # Rule 1: Save bomb for later rounds if losing
    if state.round_number >= 2 and not state.bot_bomb_used:
        if state.user_score > state.bot_score:
            return "bomb"

    # Rule 2: Counter repeated user move
    if user_move and state.last_user_move == user_move:
        counter = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }
        return counter[user_move]

    # Rule 3: Normal random behavior
    moves = list(VALID_MOVES)
    if state.bot_bomb_used:
        moves.remove("bomb")
    return random.choice(moves)


# ✅ GOOGLE ADK AGENT
agent = Agent(
    name="rps_plus_referee",
    description="AI referee for Rock-Paper-Scissors-Plus",
    tools=[
        validate_move,
        resolve_round,
        update_game_state
    ]
)


def main():
    state = GameState()
    explain_rules()

    # CLI conversational loop
    while not state.game_over:

        # 🔒 SAFETY GUARD: hard stop after max rounds
        if state.round_number > 3:
            state.game_over = True
            break

        print(f"\n--- Round {state.round_number} ---")

        user_input = input("Your move: ")

        # Tool: validate move
        validation = validate_move(
            move=user_input,
            player="user",
            state=state
        )

        if validation["status"] == ValidationStatus.INVALID:
            print(f"Invalid move: {validation['reason']}")
            state.round_number += 1
            continue

        user_move = validation["move"]

        # Bot move with adaptive strategy
        bot_move = get_bot_move(state, user_move)

        # Tool: resolve round
        result = resolve_round(
            user_move=user_move,
            bot_move=bot_move
        )

        # Tool: update game state
        state = update_game_state(
            state=state,
            user_move=user_move,
            bot_move=bot_move,
            winner=result["winner"].value
        )

        # Track last user move for strategy
        state.last_user_move = user_move

        print(f"You played: {user_move}")
        print(f"Bot played: {bot_move}")
        print(f"Result: {result['explanation']}")
        print(f"Score → You: {state.user_score} | Bot: {state.bot_score}")

    print("\n=== Game Over ===")
    if state.user_score > state.bot_score:
        print("🎉 You win!")
    elif state.bot_score > state.user_score:
        print("🤖 Bot wins!")
    else:
        print("🤝 It's a draw!")


if __name__ == "__main__":
    main()

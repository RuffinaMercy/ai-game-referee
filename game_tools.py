from typing import Dict

from game_state import GameState
from constants import VALID_MOVES, WIN_RULES, MAX_ROUNDS
from enums import ValidationStatus, RoundWinner


def validate_move(move: str, player: str, state: GameState) -> Dict:
    """
    Validate a move and enforce bomb usage rules.
    Returns structured validation status.
    """
    move = move.lower().strip()

    if move not in VALID_MOVES:
        return {
            "status": ValidationStatus.INVALID,
            "reason": "Invalid move"
        }

    if move == "bomb":
        if player == "user" and state.user_bomb_used:
            return {
                "status": ValidationStatus.INVALID,
                "reason": "User already used bomb"
            }
        if player == "bot" and state.bot_bomb_used:
            return {
                "status": ValidationStatus.INVALID,
                "reason": "Bot already used bomb"
            }

    return {
        "status": ValidationStatus.VALID,
        "move": move
    }


def resolve_round(user_move: str, bot_move: str) -> Dict:
    """
    Resolve a round and determine the winner using structured output.
    """
    if user_move == "bomb" and bot_move == "bomb":
        return {
            "winner": RoundWinner.DRAW,
            "explanation": "Both used bomb. It's a draw."
        }

    if user_move == "bomb":
        return {
            "winner": RoundWinner.USER,
            "explanation": "Bomb beats all moves."
        }

    if bot_move == "bomb":
        return {
            "winner": RoundWinner.BOT,
            "explanation": "Bomb beats all moves."
        }

    if user_move == bot_move:
        return {
            "winner": RoundWinner.DRAW,
            "explanation": "Both chose the same move."
        }

    if WIN_RULES[user_move] == bot_move:
        return {
            "winner": RoundWinner.USER,
            "explanation": f"{user_move} beats {bot_move}."
        }

    return {
        "winner": RoundWinner.BOT,
        "explanation": f"{bot_move} beats {user_move}."
    }


def update_game_state(
    state: GameState,
    user_move: str,
    bot_move: str,
    winner: str
) -> GameState:
    """
    Update game state after a round.
    """
    if user_move == "bomb":
        state.user_bomb_used = True

    if bot_move == "bomb":
        state.bot_bomb_used = True

    if winner == RoundWinner.USER.value:
        state.user_score += 1
    elif winner == RoundWinner.BOT.value:
        state.bot_score += 1

    state.round_number += 1

    if state.round_number > MAX_ROUNDS:
        state.game_over = True

    return state

# AI Game Referee – Rock–Paper–Scissors–Plus

## Overview
This project implements a minimal conversational AI referee for a best-of-3
Rock–Paper–Scissors–Plus game. The chatbot enforces game rules, tracks state
across turns, and provides clear round-by-round feedback in a CLI-style
conversational loop.

The solution is designed to evaluate logical reasoning, state modeling,
agent design, and explicit usage of Google ADK primitives.

---

## State Model
Game state is represented using a dedicated `GameState` dataclass that persists
across turns and acts as the single source of truth. It tracks:

- Current round number (1–3)
- User score and bot score
- Bomb usage per player
- Last user move (for basic bot strategy)
- Game completion status

State is not stored in the prompt and is mutated only through explicit tools,
ensuring predictable and testable behavior.

---

## Agent & Tool Design (Google ADK Usage)
The system is built using Google ADK with a clear separation of concerns:

### Agent
A single Google ADK agent acts as the game referee. Its responsibility is to:
- Orchestrate the conversational flow
- Invoke tools for validation, rule resolution, and state updates
- Generate user-facing responses

The agent does not contain game logic itself and remains focused on coordination.

### Tools
Core game logic is implemented as explicit ADK tools:
- `validate_move`: Validates user input and enforces bomb usage rules
- `resolve_round`: Determines the outcome of each round
- `update_game_state`: Mutates the game state after each round

All validation, rule enforcement, and state mutation occur inside tools rather
than in the agent logic.

---

## Design Decisions & Tradeoffs
- **Single-Agent Design**:  
  A single referee agent is sufficient for this problem scope and avoids
  unnecessary complexity.

- **Explicit State Management**:  
  Game state is modeled using a dataclass instead of implicit prompt memory,
  preventing hidden state and improving reliability.

- **Tool-Centric Game Logic**:  
  Game rules and state updates are handled through tools to keep the agent
  lightweight and easy to reason about.

- **CLI Conversational Loop**:  
  A command-line interface was chosen to focus on correctness, agent behavior,
  and state handling rather than UI complexity.

- **Minimal but Correct ADK Usage**:  
  Google ADK is used for agent structuring and tool registration while remaining
  compatible with the public SDK.

---

## Failure Handling & Safety
The system is designed to be robust against invalid or unexpected input:

- Invalid inputs are handled gracefully and waste the round without crashing
- Bomb usage is strictly limited to once per player
- The game always ends after three rounds with an explicit safety guard
- State integrity is preserved through controlled, tool-based updates

These guarantees ensure predictable and safe conversational behavior.

---

## What I Would Improve With More Time
- Introduce more advanced but explainable bot strategies
- Further formalize tool outputs using structured schemas
- Enhance the conversational UX while preserving the same core logic

---

## How to Run
```bash
pip install google-adk
python game_agent.py

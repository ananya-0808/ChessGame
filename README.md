# Chess

A two-player chess game built in Python with [Pygame](https://www.pygame.org/). Players take turns on the same computer by clicking pieces and squares. The engine generates legal moves and rejects any move that would leave your own king in check.

> **Status:** work in progress. The core move rules work, but some special rules are not implemented yet (see [Roadmap](#roadmap)).

## Features

- 8x8 board rendered with Pygame, with piece images
- Click-to-move: click a piece, then click its destination
- Move generation for pawns, knights, bishops, rooks, queens and kings
- Check detection: moves that leave your king attacked are filtered out
- Undo the last move with `Z`
- Moves printed to the console in simple coordinate notation (e.g. `e2e4`)

## Getting Started

### Requirements

- Python 3.8+
- Pygame

### Install and run

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install pygame
python ChessMain.py
```

## How to Play

| Action | Control |
| --- | --- |
| Select a piece | Left-click it |
| Move the piece | Left-click the destination square |
| Deselect | Click the selected square again |
| Undo last move | Press `Z` |

White moves first. Illegal moves are ignored.

## Project Structure

```
.
├── ChessMain.py      # Driver: handles input and draws the board and pieces
├── ChessEngine.py    # Game logic: board state, move generation, move log
└── images/           # Piece images (wp.png, bR.png, etc.)
```

- **`ChessEngine.GameState`** stores the board (an 8x8 list of two-character strings like `"wK"` or `"bp"`), the move log, and whose turn it is. It generates all moves, then filters them for legality.
- **`ChessEngine.Move`** represents a single move and can convert it to chess notation.
- **`ChessMain`** runs the game loop, translates mouse clicks into moves, and renders the current state.


## Acknowledgments

Built as a learning project following a Pygame chess engine tutorial series.

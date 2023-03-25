# Distributed tic-tac-toe

The goal is to implement the classical tic-tac-toe game following a distributed design. The game is played by two players, each one in a different machine. The game is played in rounds, where each player makes a move in their turn. The game ends when one of the players wins or when there is a draw.

To manage time syncronization we use Berkeley's algorithm.

And for leader election we use the Bully algorithm.

## Installation

### Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the dependencies, use the following command:

```bash
poetry install
```

### Pytest

This project uses pytest for testing. To run the tests, use the following command:

```bash
poetry run pytest -v
```

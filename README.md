# Chess Game and Engine
An implementation of Chess with a player vs Computer (Engine). 
Evaluating correct and valud moves and the Wngine choose to play the best move based on it's calculations. Compared with Stockfish the chess game engine that has the highest elo in the world we evaluate our chess engine and how efficient it is on evaluating the best move.

<p align="center">
    <img src="demo.png" alt="Demo" width="350" height="350">
</p>

## File Structure 
- `Chess.com API`: [Published-Data API from Chess.com](https://www.chess.com/news/view/published-data-api#pubapi-general) is a read-only REST API that has information such as player data, game data, and club/tournament information. 
    - [Documentation](https://chesscom.readthedocs.io/en/latest/)
    - Gather already established games from reputable chess players that have also been evaluated by "human" chess theory.
- `Stockfish Python Library`: The evaluation of games using the stockfish python library compared with our chess game engine.
    - [Documentation](https://pypi.org/project/stockfish/#description)
- `Chess Game`: The whole implementation of the chess game (pygame) and the game engine with use of algorithm Alpha Beta Pruning for evaluatins the best move.
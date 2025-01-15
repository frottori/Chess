# Chess Game and Engine
An implementation of Chess with a player vs Computer (Engine). 
Evaluating correct and valud moves and the Wngine choose to play the best move based on it's calculations. Compared with Stockfish chess game engine that has the highest elo in the world we evaluate our chess engine and how efficient it is on evaluating the best move.

<img src="demo.png" alt="Demo" width="300" height="300">

## File Structure 
- `Chess.com API`: [Published-Data API from Chess.com](https://www.chess.com/news/view/published-data-api#pubapi-general) is a read-only REST API that has information such as player data, game data, and club/tournament information. 
    - [Documentation](https://chesscom.readthedocs.io/en/latest/)
    - Use: Gather already established games from reputable chess players that have been also been evaluated by "human" logic to compare.
- `Stockfish Python Library`: The evaluation of games using the stockfish python library compared with out chess game engine
    - [Documentation](https://pypi.org/project/stockfish/#description)
- `Chess Game`: The whole implemenation of the chess game (pygame) and the game engine that computer uses against the player


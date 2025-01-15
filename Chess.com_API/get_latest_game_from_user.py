import requests
import datetime

def get_latest_game_pgn(username):
    today = datetime.date.today()
    year, month = today.year, today.month
    
    while True:
        # Construct the URL for the current year and month
        url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        print(f"Fetching from: {url}")  
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print(f"Games found for {username} in {year}-{month:02d}.")
            data = response.json()
            games = data.get("games", [])
            
            if games:
                # Return the PGN of the latest game
                return games[-1].get("pgn")
            else:
                print(f"No games found for {username} in {year}-{month:02d}. Trying previous month...")
        
        # Move to the previous month
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        
        # Stop if games are not found for the current year
        if year < 2024:
            print("No games found.")
            return None

# Test with Magnus Carlsen's username
username = input("Enter the Chess.com username: ")
if username == "":
    username = 'magnuscarlsen'
    
print(f"Fetching latest game for {username}...")
pgn = get_latest_game_pgn(username)

if pgn:
    with open(f"PGNs/{username}_latest_game.pgn", "w") as file:
        file.write(pgn)
    print(f"PGN saved to {username}_latest_game.pgn")
else:
    print("No games available.")

# https://www.chess.com/member/magnuscarlsen
# https://api.chess.com/pub/player/magnuscarlsen/games/2024/12
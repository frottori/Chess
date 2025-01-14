from chessdotcom import get_leaderboards, get_player_game_archives
import chessdotcom
import warnings
import pprint
import requests

# Suppress the warning about the User-Agent header
warnings.filterwarnings("ignore", category=UserWarning)
# Set the User-Agent header
chessdotcom.Client.request_config['headers']['User-Agent'] = 'My Python Application. Contact me at frossovarsou@gmail.com'

printer = pprint.PrettyPrinter()

def print_leaderboards():
    data = get_leaderboards().json
    categories = data.keys()

    for category in categories:
        print("Category:", category)
        for idx, entry in enumerate(data[category]):
            print(entry)
            # username = entry["username"]
            # score = entry["score"]
            # print(f'Rank: {idx+1} | Username: {username} | Rating: {score}')

    # if 'daily' exists, print it specifically
    if 'daily' in data:
        printer.print(data['daily'])
    else:
        print("Key 'daily' not found in the JSON response.")

def print_player_game_archives():
    headers = {"User-Agent": "My-Application/1.0"}
    data = get_player_game_archives("frottorii").json
    url = data['archives'][-1] # All games in last month
    games = requests.get(url,headers=headers).json()
    print(games)

if __name__ == "__main__":
    print_leaderboards()
    # print_player_game_archives()
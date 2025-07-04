import prompt_toolkit as pt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
import sys

def generate_completer(game_list):
    g_list = [x['name'] for x in game_list] + [x['appid'] for x in game_list]
    g_list.append("q")
    g_list.append("quit")
    g_list.append("all")
    return FuzzyCompleter(WordCompleter(g_list))

class PromptHelper:
    def __init__(self, game_list):
        self.game_list = game_list
        self.completer = generate_completer(game_list)

    def find_game_str(self, game_name):
        for game in self.game_list:
            if game['name'] == game_name:
                return game
    def find_game_num(self, appid: str):
        for game in self.game_list:
            if game['appid'] == appid:
                return game
        print("Game not found")
        return None

    def prompt_game(self, text, default="None"):
        try:
            response = pt.prompt(text, completer=self.completer, complete_while_typing=True)
        except KeyboardInterrupt:
            print("\nCtrl+C received. Exiting.")
            sys.exit(0)
        try:
            if response == "":
                return None
            elif response == "all":
                return "fetch_all_games"
            elif response == "q" or response == "quit":
                print("Goodbye!")
                sys.exit(0)
            elif response[0].isalpha():
                return self.find_game_str(response)
            else:
                return self.find_game_num(response)
        except ValueError:
            print("Invalid input")
            return None

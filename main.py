# CLI app to find Steam game paths with Compatdata
from rich import print
from prompt_toolkit import prompt
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
import vdfparser as vd
from prompt_helper import PromptHelper

class SteamGamePathTool:
    def __init__(self):
        self.steam_path = vd.fetch_steam_path()
        self.steam_vdf_path = vd.fetch_steam_vdf()

        if self.steam_vdf_path is None:
            print("Steam VDF file not found")
            # Add user input to attempt to find
            self.steam_vdf_path = prompt("Enter the path to the Steam VDF file: ", default=self.steam_path)

        self.steam_vdf = vd.parse_vdf(self.steam_vdf_path)
        self.steam_library_locations = vd.find_extra_locations(self.steam_vdf)

        for library in self.steam_library_locations:
            print(f"[+] Found Steam library at: {library}")

        games = vd.fetchall_vdfs(self.steam_vdf)
        games = self.sort_games(games)

        console = Console()
        game_rend = [Panel(self.get_game_content(game), expand=True) for game in games]
        console.print(Columns(game_rend))

        self.prompter = PromptHelper(games)
        while True:
            self.prompt_user()
            input("Press Enter to continue...")


    def prompt_user(self):
        game = self.prompter.prompt_game(text="Input (game name | appid | q/quit): ")
        if game is None:
            return
        console = Console()
        console.print(Panel(self.get_game_content(game), expand=True))


    def sort_games(self, games):
        return sorted(games, key=lambda x: x['name'])

    def get_game_content(self, game):
        """
        Takes a game dictionary and returns a string that formats game information into a string renderable by the console in the rich library.

        :param game: A dictionary containing information about a Steam game
        :return: string formatted for table using rich library
        """
        # Spaces must be replaced with %20 otherwise they won't link properly

        string = f"""[b]{game['name']}[/b]
        [white]Game ID: [yellow]{game['appid']}
        [white]Game Size: [red]{int(game['SizeOnDisk'])/(1024*1024)/1024:.2f} GB[/red]
        [white]Game acf: [green][link=file://{game['acf_path'].replace(' ', '%20')}]file[/link][/green]
        [white]Game Path: [green][link=file://{game['true_path'].replace(' ', '%20')}]dir[/link][/green]"""
        if game['compatdata_path']:
            string += f"\n\t[white]Compatdata dir: [blue][link=file://{game['compatdata_path'].replace(' ', '%20')}]dir[/link][/blue]"
        return string
if __name__ == "__main__":
    steam_path_tool = SteamGamePathTool()

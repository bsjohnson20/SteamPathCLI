# CLI app to find Steam game paths with Compatdata
from rich import print
from prompt_toolkit import prompt
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
import src.vdfparser as vd
from src.prompt_helper import PromptHelper

class TableItem:
    def __init__(self, name, data='', colour='white', type='desc'):
        self.name = name
        self.data = data
        self.type = type
        self.colour = colour

    def generate_link(self):
        if self.type == 'file':
            return f"[{self.colour}][link=file://{self.data}]file[/link][/{self.colour}]"
        elif self.type == 'dir':
            return f"[{self.colour}][link=file://{self.data}]dir[/link][/{self.colour}]"
        else:
            return f"[{self.colour}]{self.data}[/{self.colour}]"

    def __str__(self):
        return f"\n[white]{self.name}[/white]: [{self.colour}]"+self.generate_link()+""

class SteamGamePathTool:
    def __init__(self):
        self.steam_path = vd.fetch_steam_path()
        self.steam_vdf_path = vd.fetch_steam_vdf()

        if self.steam_vdf_path is None:
            print("Steam VDF file not found")
            # Add user input to attempt to find
            self.steam_vdf_path = prompt("Enter the path to the Steam VDF file: ", default=self.steam_path)

        # Fetch steam's vdf file and convert to json dict
        self.steam_vdf = vd.parse_vdf(self.steam_vdf_path)
        # Possible other locations where steamlibrary could be found
        self.steam_library_locations = vd.find_extra_locations(self.steam_vdf)

        games = vd.fetchall_vdfs(self.steam_vdf)
        self.games = self.sort_games(games)

        for library in self.steam_library_locations:
            print(f"[+] Found Steam library at: {library}")

        self.prompter = PromptHelper(games)
        while True:
            self.prompt_user()
            try:
                input("Press Enter to continue...")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    def prompt_user(self):
        game = self.prompter.prompt_game(text="Input (game name | appid | all | q/quit): ")
        if game is None:
            return
        elif game == 'fetch_all_games':
            console = Console()
            game_rend = [Panel(self.get_game_content(game), expand=True) for game in self.games]
            console.print(Columns(game_rend))
        else:
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

        string = f"""[b]{game['name']}[/b]"""
        string+=str(TableItem(name="Game ID", data=game['appid'], colour="yellow",type="desc"))
        string+=str(TableItem(name="Game Size", data=f"{int(game['SizeOnDisk'])/(1024*1024)/1024:.2f} GB", colour="red",type="desc"))
        string+=str(TableItem(name="Game acf", data=f"{game['acf_path'].replace(' ', '%20')}", colour="green",type="dir"))
        string+=str(TableItem(name="Game Path", data=f"{game['true_path'].replace(' ', '%20')}", colour="blue",type="dir"))
        if game['workshop_path']:
            string+=str(TableItem(name="Game Workshop Path", data=f"{game['workshop_path'].replace(' ', '%20')}", colour="blue", type="dir"))
        if game["compatdata_path"]:
            string+=str(TableItem(name="Game Compatdata Path",data=f"{game['compatdata_path'].replace(' ', '%20')}",colour="blue",type="dir"))
        return string

if __name__ == "__main__":
    steam_path_tool = SteamGamePathTool()

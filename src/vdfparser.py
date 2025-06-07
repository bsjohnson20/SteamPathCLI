import os
import vdf

def parse_vdf(steam_vdf_path) -> dict:
    """
    Reads the Steam vdf file at the given path and returns the corresponding dict.

    :param steam_vdf_path: Path to the Steam vdf file
    :return: Dict representing the vdf data
    """
    vdf_data = vdf.loads(open(steam_vdf_path, 'r').read())
    return vdf_data

def fetch_ids(vdf_json: dict):
    """
    Prints all Steam app IDs from the given vdf data.

    :param vdf_json: vdf data as a dict
    """
    for library in vdf_json["libraryfolders"]:
        print(f"Library {library}: {vdf_json['libraryfolders'][library]['apps']}")
        for app_id in vdf_json['libraryfolders'][library]['apps']:
            print(f"{app_id}")
        print()

def fetch_steam_path() -> str:
    """
    Determines the Steam installation path by checking common locations.

    Returns the path to the Steam 'steamapps' directory.
    Prefers the path used by the apt installation if it exists.
    Otherwise, returns the path used by the Flatpak installation.

    :return: Path to the Steam 'steamapps' directory
    """

    apt_steam_path = os.path.expanduser(r"~/.steam/steam/steamapps/")
    flatpak_steam_path = os.path.expanduser(r"~/.var/app/com.valvesoftware.Steam/data/Steam/steamapps/")
    return apt_steam_path if os.path.exists(apt_steam_path) else flatpak_steam_path

def fetch_steam_vdf() -> str | None:
    """
    Determines the path to the Steam libraryfolders.vdf file by checking common locations.

    Returns the path to the libraryfolders.vdf file if it exists.
    Otherwise, returns None.

    :return: Path to the libraryfolders.vdf file or None
    """
    steam_vdf_path = os.path.join(fetch_steam_path(), "libraryfolders.vdf")
    return steam_vdf_path if os.path.exists(steam_vdf_path) else None

def validate_steam_path(path) -> bool:
    if not os.path.exists(path):
        print(f"Steam path does not exist (could be not mounted): {path}")
        return False
    return True

# Scans vdf file for additional steam library paths... e.g. USB drive, external HDD
def find_extra_locations(vdf_json):
    """
    Scans the vdf_json for additional Steam library paths and validates them.

    :param vdf_json: A dictionary representing the parsed Steam VDF data.
    :return: A list of valid paths to additional Steam library locations.
    """

    steam_library_locations = []
    for library in vdf_json["libraryfolders"]:
        path = vdf_json['libraryfolders'][library]['path']
        # print(path)
        if validate_steam_path(path):
            steam_library_locations.append(path)
        else:
            print(f"[-] Invalid Steam path: {path}")
    return steam_library_locations

# Reads manifest of individual game vdfs
def read_game_vdf(gameID: int, steam_vdf_json: dict, path, game) -> dict:
    with open(os.path.join(path, game), 'r') as f:
        game_vdf = vdf.loads(f.read())
    return game_vdf['AppState']

def fetchall_vdfs(steam_vdf_json: dict):
    """
    Reads all Steam game manifests in the given Steam VDF data and returns a list of dictionaries containing information about each game.

    :param steam_vdf_json: A dictionary representing the parsed Steam VDF data.
    :return: A list of dictionaries containing information about each Steam game.
    """
    games = []
    for library in steam_vdf_json["libraryfolders"]:
        path = steam_vdf_json['libraryfolders'][library]['path']
        steamapps = os.path.join(path, "steamapps")
        for game in os.listdir(steamapps):
            if game.endswith(".acf"):
                gameID = int(game.split('.')[0].split('_')[1])
                parsed_game = read_game_vdf(gameID, steam_vdf_json, steamapps, game)
                parsed_game['acf_path'] = os.path.join(steamapps, game)
                parsed_game['root_steam_folder'] = path
                parsed_game['true_path'] = os.path.join(steamapps, "common", parsed_game['installdir'])
                parsed_game['compatdata_path'] = os.path.join(steamapps, "compatdata", str(gameID)) if os.path.exists(os.path.join(steamapps, "compatdata", str(gameID))) else None
                parsed_game['workshop_path'] = os.path.join(steamapps, "workshop", "content", str(gameID)) if os.path.exists(os.path.join(steamapps, "workshop", "content", str(gameID))) else ""
                games.append(parsed_game)
                # print("Game name:", parsed_game['name'], "ID:", gameID, "Path:", parsed_game['true_path'])
    return games

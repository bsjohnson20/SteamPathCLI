# Steam Game Path View

Prints a table showcasing where the compatfolder, install folder and size of games installed on the system

## Quick overview

Minor note some terminals can't open the hyperlinks properly (konsole)

Each box has a hyperlink which opens the folder/file, using a embedded hyperlink in order to reduce
the size of the boxes and have consistency

1. finds installed steam, (apt/flatpak)
2. Loads .vdf from location
3. Fetches additional steam libraries
4. Checks mounted status (to exclude things not present)
5. Reads game vdf from steam library locations for paths
6. Prints AppID with steam path and game name in addition to compatdata folder


## Installation

Install packages with
``uv sync``

Run with
``uv run main.py``



## Video recording

[![asciicast](https://asciinema.org/a/qfN1Nc4Sy7swPJVXUeWsmSDqx.svg)](https://asciinema.org/a/qfN1Nc4Sy7swPJVXUeWsmSDqx)

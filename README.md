# Halite III Rank Visualizer
## Synopsis
The Halite Rank Visualizer is a Python 3 program that neatly graphs any Halite 3 user's rank over time.
## How to Use
### Downloading
The Visualizer can be downloaded one of two ways:
1. The first is downloading one of the pre-built binaries from the release page\(not yet implemented).
2. The other is `git clone https://github.com/zPaw/halite-III-rank-visualizer.git` 
   - This method requires the use of the command `pip install -r requirements.txt` to install all dependencies

Both of these methods require some setup in the `config.json`.
### Configuring
The following are found in the `config.json`.
1. The `user_ids` key is the list of user ids which are found at the end of any given user's profile page url.
2. The `interval` key is how many seconds the program will wait before polling the api and updating the information on screen

import json


def save_data(name: str, perfectionist: bool, guesses: int, intractable_time_sec: int, total_time_sec: int) -> None:
    """Saves game data as JSON dict if new player name or new high score.

    :param name: Player's name.
    :param perfectionist: Self-described perfectionist boolean.
    :param guesses: Total number of guesses made for unsolvable puzzle.
    :param intractable_time_sec: Total number of seconds spent trying to solve intractable puzzle.
    :param total_time_sec: Total number of seconds spent playing the game until completion.
    """
    def write_to_file():
        pass

    with open('word_game/game_data.json') as f:
        data = json.load(f)

    if data:
        player_data = data.get(name)
        if not player_data:
            write_to_file()
        else:
            if player_data['score'] < total_time_sec and player_data[name] != 'Player 1':
                write_to_file()
    else:
        # Create the data file
        pass


def load_scoreboard() -> dict:
    """Readers scores.json file and returns a dictionary to display at the end of each game."""
    pass

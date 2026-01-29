import os
import pandas as pd

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

def load_games(season: int):
    path = os.path.join(get_project_root(), f"data/manual/games/games_{season}.csv")
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

def load_pbp(game_id: int):
    path = os.path.join(get_project_root(), f"data/manual/pbp/pbp_{game_id}.csv")
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

def load_odds(game_id: int):
    path = os.path.join(get_project_root(), f"data/manual/odds/odds_{game_id}.csv")
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

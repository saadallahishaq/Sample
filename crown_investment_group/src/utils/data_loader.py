import os
import pandas as pd

def load_games(season: int) -> pd.DataFrame:
    candidates = [f"data/games/games_{season}.csv", f"data/curated/games_{season}.csv", f"data/manual/games/games_{season}.csv"]
    for path in candidates:
        if os.path.exists(path): return pd.read_csv(path)
    return pd.DataFrame()

def load_pbp(game_id: int) -> pd.DataFrame:
    candidates = [f"data/pbp/pbp_{game_id}.csv", f"data/curated/pbp_{game_id}.csv", f"data/manual/pbp/pbp_{game_id}.csv"]
    for path in candidates:
        if os.path.exists(path): return pd.read_csv(path)
    return pd.DataFrame()

def load_odds(game_id: int) -> pd.DataFrame:
    candidates = [f"data/odds/odds_{game_id}.csv", f"data/curated/odds_{game_id}.csv", f"data/manual/odds/odds_{game_id}.csv"]
    for path in candidates:
        if os.path.exists(path): return pd.read_csv(path)
    return pd.DataFrame()

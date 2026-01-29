from __future__ import annotations
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import requests

# CONFIG FOR LAKERS @ MAVS (01/24/2026)
GAME_URL = "https://www.basketball-reference.com/boxscores/202601240DAL.html"
PBP_URL  = "https://www.basketball-reference.com/boxscores/pbp/202601240DAL.html"
SEASON = 2026
GAME_ID = 2026012401
HOME_POINT_SPREAD = 4.0  # DAL +4

OUT_GAMES = Path("data/manual/games")
OUT_PBP   = Path("data/manual/pbp")
OUT_ODDS  = Path("data/manual/odds")

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NBAInGameAnalysis/1.0)"}

def fetch_html(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def parse_teams_and_date_from_game_url(game_url: str) -> tuple[str, str, str]:
    # Fixed regex: added the '0' that Basketball Reference includes before the team code
    m = re.search(r"/boxscores/(\d{8})0([A-Z]{3})\.html", game_url)
    if not m:
        raise ValueError(f"Could not parse URL: {game_url}. Check if format matches /boxscores/YYYYMMDD0TEAM.html")
    ymd, home = m.group(1), m.group(2)
    dt = datetime.strptime(ymd, "%Y%m%d")
    return dt.strftime("%Y-%m-%d"), home, ymd

def extract_away_team_from_boxscore(html: str) -> str:
    tables = pd.read_html(html)
    for t in tables:
        if t.shape[1] >= 2 and ("T" in t.columns or "Team" in t.columns):
            teams = t.iloc[:, 0].astype(str).tolist()
            cand = [x.strip() for x in teams if len(x.strip()) <= 4]
            if len(cand) >= 2: return cand[0]
    return "LAL"

def pbp_table_from_html(html: str) -> pd.DataFrame:
    tables = pd.read_html(html)
    for t in tables:
        if any("time" in str(c).lower() for c in t.columns) and t.shape[0] > 50:
            return t
    raise ValueError("PBP table not found.")

def main():
    for p in [OUT_GAMES, OUT_PBP, OUT_ODDS]: p.mkdir(parents=True, exist_ok=True)
    
    day, home_team, _ = parse_teams_and_date_from_game_url(GAME_URL)
    away_team = extract_away_team_from_boxscore(fetch_html(GAME_URL))
    raw_pbp = pbp_table_from_html(fetch_html(PBP_URL))
    raw_pbp.columns = [str(c).strip() for c in raw_pbp.columns]
    
    time_col = next(c for c in raw_pbp.columns if "time" in c.lower())
    score_col = next(c for c in raw_pbp.columns if "score" in c.lower())
    
    pbp_rows, current_q = [], 1
    for _, r in raw_pbp.iterrows():
        txt = " ".join(map(str, r.values)).lower()
        if "1st q" in txt: current_q = 1
        elif "2nd q" in txt: current_q = 2
        elif "3rd q" in txt: current_q = 3
        elif "4th q" in txt: current_q = 4
        
        tm, sc = r.get(time_col), r.get(score_col)
        if not isinstance(tm, str) or ":" not in tm: continue
        
        m_score = re.match(r"^(\d+)\s*-\s*(\d+)$", str(sc).strip())
        aw_s, hm_s = (int(m_score.group(1)), int(m_score.group(2))) if m_score else (None, None)
        min_rem, sec_rem = map(int, tm.split(":"))
        
        pbp_rows.append({
            "PlayID": len(pbp_rows)+1, "QuarterID": current_q, "Sequence": len(pbp_rows)+1,
            "TimeRemainingMinutes": min_rem, "TimeRemainingSeconds": sec_rem,
            "AwayTeam": away_team, "HomeTeam": home_team, "AwayScore": aw_s, "HomeScore": hm_s
        })
    
    pbp_df = pd.DataFrame(pbp_rows)
    pbp_df[["AwayScore", "HomeScore"]] = pbp_df[["AwayScore", "HomeScore"]].ffill().fillna(0).astype(int)
    pbp_df.to_csv(OUT_PBP / f"pbp_{GAME_ID}.csv", index=False)
    
    games_df = pd.DataFrame([{
        "GameID": GAME_ID, "Season": SEASON, "Status": "Final", "Day": day, "DateTime": f"{day}T20:00:00",
        "AwayTeam": away_team, "HomeTeam": home_team, "AwayTeamScore": int(pbp_df["AwayScore"].iloc[-1]),
        "HomeTeamScore": int(pbp_df["HomeScore"].iloc[-1]), "PointSpread": HOME_POINT_SPREAD
    }])
    games_df.to_csv(OUT_GAMES / f"games_{SEASON}.csv", index=False)
    
    # Generate Simulated Moneyline Movement
    base_dt = datetime.strptime(f"{day} 20:00:00", "%Y-%m-%d %H:%M:%S")
    odds_rows = []
    for i, offset in enumerate([0, 720, 1440, 2160, 2880]):
        odds_rows.append({
            "GameID": GAME_ID, "DateTime": (base_dt + timedelta(seconds=offset)).isoformat(),
            "GameSec": offset, "Sportsbook": "ManualBook", "HomeMoneyLine": -165 + (i*10),
            "AwayMoneyLine": 145 - (i*10), "HomeSpread": 4.0, "AwaySpread": -4.0
        })
    pd.DataFrame(odds_rows).to_csv(OUT_ODDS / f"odds_{GAME_ID}.csv", index=False)
    print(f"✅ Data for {away_team} vs {home_team} (01/24/2026) generated successfully.")

if __name__ == "__main__": main()

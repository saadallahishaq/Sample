import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.data_loader import load_games

st.set_page_config(page_title="Games | Crown Investment Group", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #FF8C00 !important; }
    .game-card { background-color: #161B22; padding: 20px; border-radius: 10px; border-left: 5px solid #FF8C00; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 Game Schedule & Analytics")
st.markdown("---")

st.sidebar.markdown("<h2 style='color: #FF8C00;'>Crown Investment Group</h2>", unsafe_allow_html=True)
season = st.sidebar.selectbox("Select Season", [2026, 2025])
df = load_games(season)

if not df.empty:
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="game-card">
            <h3>{row['AwayTeam']} @ {row['HomeTeam']}</h3>
            <p>Score: {row['AwayTeamScore']} - {row['HomeTeamScore']} | Date: {row['Day']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No games found.")

st.sidebar.info("Crown Investment Group")

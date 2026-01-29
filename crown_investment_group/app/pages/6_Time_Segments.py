import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.data_loader import load_games, load_pbp

st.set_page_config(page_title="Time Segments | Crown Investment Group", layout="wide")

st.title("⏱️ Game Time Segments")
st.markdown("---")

season = st.sidebar.selectbox("Season", [2026, 2025], index=0)
games_df = load_games(season)

if not games_df.empty:
    game_options = games_df.apply(lambda x: f"{x['GameID']} - {x['AwayTeam']} @ {x['HomeTeam']}", axis=1).tolist()
    selected = st.selectbox("Select Game", game_options)
    gid = int(selected.split(" - ")[0])
    
    pbp_df = load_pbp(gid)
    
    if not pbp_df.empty:
        pbp_df['Margin'] = pbp_df['HomeScore'] - pbp_df['AwayScore']
        fig = px.bar(pbp_df, x='Sequence', y='Margin', color='Margin',
                    title="Score Margin Throughout Game", template="plotly_dark",
                    color_continuous_scale=['#00CC96', '#FFFFFF', '#FF4B11'])
        st.plotly_chart(fig, use_container_width=True)

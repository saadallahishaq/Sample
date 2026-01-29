import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.data_loader import load_games, load_pbp

st.set_page_config(page_title="Time Segments | Crown Investment Group", layout="wide")

st.title("⏱️ Game Time Segments")
st.markdown("---")

st.sidebar.markdown("<h2 style='color: #FF8C00;'>Crown Investment Group</h2>", unsafe_allow_html=True)
season = st.sidebar.selectbox("Season", [2026, 2025])
games_df = load_games(season)

if not games_df.empty:
    gid = st.selectbox("Select Game ID", games_df['GameID'].tolist())
    pbp_df = load_pbp(gid)
    
    if not pbp_df.empty:
        st.dataframe(pbp_df, use_container_width=True)

st.sidebar.info("Crown Investment Group")

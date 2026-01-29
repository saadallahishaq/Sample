import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.data_loader import load_games, load_pbp

st.set_page_config(page_title="Game Detail | Crown Investment Group", layout="wide")

st.markdown("<style>h1, h2, h3 { color: #FF8C00 !important; }</style>", unsafe_allow_html=True)
st.title("📊 Detailed Game Analysis")
st.markdown("---")

st.sidebar.markdown("<h2 style='color: #FF8C00;'>Crown Investment Group</h2>", unsafe_allow_html=True)
season = st.sidebar.selectbox("Season", [2026, 2025])
games_df = load_games(season)

if not games_df.empty:
    selected = st.selectbox("Select Game ID", games_df['GameID'].tolist())
    pbp_df = load_pbp(selected)
    
    st.subheader(f"In-Game Scoring Summary")
    if not pbp_df.empty:
        fig = px.line(pbp_df, x='Sequence', y=['AwayScore', 'HomeScore'], template="plotly_dark", color_discrete_map={"HomeScore": "#FF8C00", "AwayScore": "#FFFFFF"})
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(pbp_df.style.highlight_max(axis=0, color='#FF8C00'), use_container_width=True)

st.sidebar.info("Crown Investment Group")

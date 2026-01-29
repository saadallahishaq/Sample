import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.utils.data_loader import load_games, load_odds

st.set_page_config(page_title="Odds | Crown Investment Group", layout="wide")

st.markdown("<style>h1, h2, h3 { color: #FF8C00 !important; } .stMetric div { color: #FF8C00 !important; }</style>", unsafe_allow_html=True)
st.title("🎲 Market Odds & Sentiment")
st.markdown("---")

st.sidebar.markdown("<h2 style='color: #FF8C00;'>Crown Investment Group</h2>", unsafe_allow_html=True)
season = st.sidebar.selectbox("Season", [2026, 2025])
games_df = load_games(season)

if not games_df.empty:
    gid = st.selectbox("Select Game ID", games_df['GameID'].tolist())
    odds_df = load_odds(gid)
    
    if not odds_df.empty:
        latest = odds_df.iloc[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("Home ML", latest['HomeMoneyLine'])
        col2.metric("Away ML", latest['AwayMoneyLine'])
        col3.metric("Current Spread", latest['HomeSpread'])
        
        st.subheader("Historical Odds Snapshots")
        st.dataframe(odds_df, use_container_width=True)

st.sidebar.info("Crown Investment Group")

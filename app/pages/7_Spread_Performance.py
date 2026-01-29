import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.data_loader import load_games, load_odds

st.set_page_config(page_title="Spread Performance | Crown Investment Group", layout="wide")

st.markdown("<style>h1, h2, h3 { color: #FF8C00 !important; }</style>", unsafe_allow_html=True)
st.title("📈 Spread Performance Analytics")
st.markdown("---")

st.sidebar.markdown("<h2 style='color: #FF8C00;'>Crown Investment Group</h2>", unsafe_allow_html=True)
season = st.sidebar.selectbox("Season", [2026, 2025])
games_df = load_games(season)

if not games_df.empty:
    gid = st.selectbox("Select Game ID", games_df['GameID'].tolist())
    odds_df = load_odds(gid)
    
    if not odds_df.empty:
        st.subheader("Spread Movement Over Time")
        fig = px.area(odds_df, x='DateTime', y='HomeSpread', template="plotly_dark", color_discrete_sequence=['#FF8C00'])
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.info("Crown Investment Group")

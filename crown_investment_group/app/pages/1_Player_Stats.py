import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.data_loader import load_games

st.set_page_config(page_title="Player Stats | Crown Investment Group", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #FF8C00 !important; }
    .stMetric label { color: #FF8C00 !important; }
    .stMetric div { color: #FFFFFF !important; font-size: 2.5rem !important; font-weight: bold !important; }
    div[data-testid="stSidebarNav"] { background-color: #161B22; }
    </style>
    """, unsafe_allow_html=True)

st.title("👤 Player Performance Analytics")
st.markdown("---")

st.sidebar.markdown("<h2 style='color: #FF8C00;'>Crown Investment Group</h2>", unsafe_allow_html=True)
season = st.sidebar.selectbox("Select Season", [2026, 2025])
games_df = load_games(season)
selected_game = st.sidebar.selectbox("Select Game ID", games_df['GameID'].tolist() if not games_df.empty else ["No Games"])

player_id = st.selectbox("Select Player ID to Analyze", ["20000603.0", "20000604.0"])

st.subheader(f"Performance Summary: Player {player_id} (DAL)")

col1, col2 = st.columns(2)
col1.metric("Total Involvements", "1")
col2.metric("Team Usage Share", "100.0%")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Involvement by Quarter")
    fig_bar = px.bar(x=['Q1', 'Q2', 'Q3', 'Q4'], y=[1, 0, 0, 0], template="plotly_dark", color_discrete_sequence=['#FF8C00'])
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Play Type Breakdown")
    fig_pie = px.pie(names=['Scrambled', 'Set Play'], values=[1, 0], template="plotly_dark", color_discrete_sequence=['#FF8C00', '#444444'])
    st.plotly_chart(fig_pie, use_container_width=True)

st.sidebar.info("Crown Investment Group")

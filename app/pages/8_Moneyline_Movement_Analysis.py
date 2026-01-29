import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.data_loader import load_games, load_odds
def american_to_implied(moneyline):
    if moneyline > 0: return 100 / (moneyline + 100)
    else: return abs(moneyline) / (abs(moneyline) + 100)
st.set_page_config(page_title="Advanced Analytics | Crown Investment Group", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stMetric { border-left: 5px solid #FF4B11 !important; padding-left: 10px; }
    h1, h2, h3 { color: #FF8C00 !important; }
    </style>
    """, unsafe_allow_html=True)
st.title("🏀 Advanced Moneyline & Spread Analytics")
st.markdown("---")
season = st.sidebar.selectbox("Select Season", [2026, 2025], index=0)
games_df = load_games(season)
if games_df.empty:
    st.warning(f"No games found for season {season}.")
else:
    game_options = games_df.apply(lambda x: f"{x['GameID']} - {x['AwayTeam']} @ {x['HomeTeam']} ({x['Day']})", axis=1).tolist()
    selected_game_str = st.selectbox("Select Game", game_options)
    selected_game_id = int(selected_game_str.split(" - ")[0])
    odds_df = load_odds(selected_game_id)
    game_info = games_df[games_df['GameID'] == selected_game_id].iloc[0]
    if odds_df.empty:
        st.error("Odds data not detected for this game.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Away Team", game_info['AwayTeam'], f"{game_info['AwayTeamScore']}")
        col2.metric("Home Team", game_info['HomeTeam'], f"{game_info['HomeTeamScore']}")
        opening_ml = odds_df.iloc[0]['HomeMoneyLine']
        closing_ml = odds_df.iloc[-1]['HomeMoneyLine']
        ml_change = closing_ml - opening_ml
        col3.metric("Home ML Shift", f"{closing_ml}", f"{ml_change:+}")
        opening_sp = odds_df.iloc[0]['HomeSpread']
        closing_sp = odds_df.iloc[-1]['HomeSpread']
        sp_change = closing_sp - opening_sp
        col4.metric("Home Spread Shift", f"{closing_sp}", f"{sp_change:+}")
        st.markdown("### Line Movement Analysis")
        tab1, tab2, tab3 = st.tabs(["💰 Moneyline Movement", "📈 Implied Probability", "🎯 Spread Movement"])
        with tab1:
            fig_ml = px.line(odds_df, x='DateTime', y=['HomeMoneyLine', 'AwayMoneyLine'], template="plotly_dark", color_discrete_map={"HomeMoneyLine": "#FF4B11", "AwayMoneyLine": "#00CC96"})
            st.plotly_chart(fig_ml, use_container_width=True)
        with tab2:
            odds_df['HomeImplied'] = odds_df['HomeMoneyLine'].apply(american_to_implied)
            odds_df['AwayImplied'] = odds_df['AwayMoneyLine'].apply(american_to_implied)
            fig_prob = go.Figure()
            fig_prob.add_trace(go.Scatter(x=odds_df['DateTime'], y=odds_df['HomeImplied'], fill='tozeroy', name="Home Win Prob", line_color='#FF4B11'))
            fig_prob.add_trace(go.Scatter(x=odds_df['DateTime'], y=odds_df['AwayImplied'], fill='tonexty', name="Away Win Prob", line_color='#00CC96'))
            fig_prob.update_layout(template="plotly_dark", yaxis_tickformat='.1%', hovermode="x unified")
            st.plotly_chart(fig_prob, use_container_width=True)
        with tab3:
            fig_sp = px.area(odds_df, x='DateTime', y='HomeSpread', template="plotly_dark", color_discrete_sequence=['#FF4B11'])
            st.plotly_chart(fig_sp, use_container_width=True)
        with st.expander("Detailed Odds Log"):
            st.dataframe(odds_df, use_container_width=True)
st.sidebar.info("Crown Investment Group")

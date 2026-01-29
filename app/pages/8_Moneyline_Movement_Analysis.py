import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# FOOLPROOF IMPORT FIX: Add project root to sys.path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if root not in sys.path:
    sys.path.insert(0, root)

from src.utils.data_loader import load_games, load_odds

def american_to_implied(ml):
    return (100 / (ml + 100)) if ml > 0 else (abs(ml) / (abs(ml) + 100))

st.set_page_config(page_title="Advanced Analytics | Crown Investment Group", layout="wide")
st.markdown("<style>.main { background-color: #0E1117; } .stMetric { border-left: 5px solid #FF4B11; padding-left: 10px; } h1, h2, h3 { color: #FF8C00 !important; }</style>", unsafe_allow_html=True)

st.title("🏀 Advanced Moneyline & Spread Analytics")
st.markdown("---")

season = st.sidebar.selectbox("Select Season", [2026, 2025], index=0)
games_df = load_games(season)

if games_df.empty:
    st.warning(f"No games found for season {season}.")
else:
    game_opts = games_df.apply(lambda x: f"{x['GameID']} - {x['AwayTeam']} @ {x['HomeTeam']}", axis=1).tolist()
    sel_game = st.selectbox("Select Game", game_opts)
    gid = int(sel_game.split(" - ")[0])
    odds_df = load_odds(gid)
    info = games_df[games_df['GameID'] == gid].iloc[0]

    if odds_df.empty:
        st.error("Odds data not detected.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Away Team", info['AwayTeam'], info['AwayTeamScore'])
        c2.metric("Home Team", info['HomeTeam'], info['HomeTeamScore'])
        c3.metric("Home ML", odds_df.iloc[-1]['HomeMoneyLine'])
        c4.metric("Home Spread", info['PointSpread'])

        t1, t2, t3 = st.tabs(["💰 Moneyline", "📈 Probability", "🎯 Spread"])
        with t1:
            st.plotly_chart(px.line(odds_df, x='DateTime', y=['HomeMoneyLine', 'AwayMoneyLine'], template="plotly_dark", color_discrete_map={"HomeMoneyLine": "#FF4B11", "AwayMoneyLine": "#00CC96"}), use_container_width=True)
        with t2:
            odds_df['HomeProb'] = odds_df['HomeMoneyLine'].apply(american_to_implied)
            odds_df['AwayProb'] = odds_df['AwayMoneyLine'].apply(american_to_implied)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=odds_df['DateTime'], y=odds_df['HomeProb'], fill='tozeroy', name="Home Prob", line_color='#FF4B11'))
            fig.add_trace(go.Scatter(x=odds_df['DateTime'], y=odds_df['AwayProb'], fill='tonexty', name="Away Prob", line_color='#00CC96'))
            fig.update_layout(template="plotly_dark", yaxis_tickformat='.1%')
            st.plotly_chart(fig, use_container_width=True)
        with t3:
            st.plotly_chart(px.area(odds_df, x='DateTime', y='HomeSpread', template="plotly_dark", color_discrete_sequence=['#FF4B11']), use_container_width=True)
        st.dataframe(odds_df, use_container_width=True)

st.sidebar.info("Crown Investment Group")

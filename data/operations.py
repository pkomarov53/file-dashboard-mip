import pandas as pd
import sqlite3
import streamlit as st

DB_PATH = 'data/cache/feedback.db'

@st.cache_data
def load_data_from_db() -> pd.DataFrame:
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM feedback", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Ошибка чтения базы данных: {e}")
        return pd.DataFrame()
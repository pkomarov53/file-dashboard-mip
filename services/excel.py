# Обработка загружаемого .xlsx файла
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path: str):
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Файл '{file_path}' не найден.")
        return None
    except Exception as e:
        st.error(f"Ошибка при чтении Excel файла: {e}")
        return None
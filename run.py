# Запуск приложения
import streamlit as st
import os
from data.initialize import init_db
from data.operations import load_data_from_db
from services.filters import apply_filters
from services.visualize import render_dashboard

# Настройка страницы без смайликов
st.set_page_config(
    page_title="Аналитика: Психологическое консультирование", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # 1. Загрузка данных в БД из Excel
    excel_path = "2026-08-04 Обратная связь по прохождению модуля Психконс.xlsx"
    if os.path.exists(excel_path):
        init_db(excel_path)
    else:
        st.error(f"Файл '{excel_path}' не найден в корневой папке.")
        return

    # 2. Получение данных из БД
    df = load_data_from_db()
    
    if not df.empty:
        # 3. Фильтры
        filtered_df = apply_filters(df)
        
        # 4. Отрисовка
        render_dashboard(filtered_df)
    else:
        st.warning("База данных пуста или произошла ошибка при загрузке.")

if __name__ == "__main__":
    main()
# Запуск приложения
import streamlit as st
import os
from data.initialize import init_db
from data.operations import load_data_from_db
from services.filters import apply_filters
from services.visualize import render_dashboard

st.set_page_config(
    page_title="Аналитика: Психологическое консультирование", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    excel_feedback = "2026-08-04 Обратная связь по прохождению модуля Психконс.xlsx"
    excel_intro = "2026-08-05 Обратная связь в начале обучения.xlsx"
    db_path = "data/cache/feedback.db"
    
    if os.path.exists(excel_feedback) and os.path.exists(excel_intro):
        # Пересоздаем БД только при ее отсутствии или при обновлении исходных Excel-файлов
        if not os.path.exists(db_path):
            init_db(excel_feedback, excel_intro)
        else:
            db_mtime = os.path.getmtime(db_path)
            excel_mtime = max(os.path.getmtime(excel_feedback), os.path.getmtime(excel_intro))
            if excel_mtime > db_mtime:
                init_db(excel_feedback, excel_intro)
    else:
        st.error("Один или оба файла Excel не найдены в корневой папке.")
        return

    # Получение объединенных данных из БД
    df = load_data_from_db()
    
    if not df.empty:
        filtered_df = apply_filters(df)
        render_dashboard(filtered_df)
    else:
        st.warning("База данных пуста или произошла ошибка при загрузке.")

if __name__ == "__main__":
    main()
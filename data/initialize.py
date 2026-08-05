# Инициализация базы данных
import pandas as pd
import sqlite3
import os

DB_PATH = 'data/cache/feedback.db'

def init_db(feedback_path: str, intro_path: str):
    os.makedirs('data/cache', exist_ok=True)
    
    try:
        df_feedback = pd.read_excel(feedback_path)
        df_intro = pd.read_excel(intro_path)
        
        demo_cols = [
            'userId', 
            'Укажите Ваш пол', 
            'Укажите Ваш возраст', 
            'Имеется ли у вас психологическое образование?'
        ]
        
        df_intro_clean = df_intro.dropna(subset=['userId'])[demo_cols].drop_duplicates(subset=['userId'], keep='last')
        df_merged = df_feedback.merge(df_intro_clean, on='userId', how='left')
        
        # Гарантированное закрытие соединения после записи
        with sqlite3.connect(DB_PATH) as conn:
            df_merged.to_sql('feedback', conn, if_exists='replace', index=False)
            
        print("Данные успешно объединены и обновлены в локальной базе.")
        
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
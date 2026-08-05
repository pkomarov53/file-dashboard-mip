# Инициализация базы данных
# Переносит данные из .xlsx в .db
import pandas as pd
import sqlite3
import os

# Путь к локальной БД
DB_PATH = 'data/cache/feedback.db'

def init_db(excel_file_path: str):
    # Создаем папку data/cache, если её нет
    os.makedirs('data/cache', exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Проверяем, существует ли уже таблица feedback
        cursor = conn.cursor()
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedback'")
        if cursor.fetchone()[0] == 1:
            return # Данные уже загружены, пропускаем инициализацию
        
        # Если таблицы нет, считываем Excel и заливаем в БД
        df = pd.read_excel(excel_file_path)
        
        # Сохраняем в таблицу 'feedback' (заменяем, если есть)
        df.to_sql('feedback', conn, if_exists='replace', index=False)
        print("Данные успешно скопированы в локальную базу.")
        
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
    finally:
        conn.close()
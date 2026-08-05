# Обработка загружаемого .xlsx файла
import pandas as pd

def read_excel_safely(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return pd.DataFrame()
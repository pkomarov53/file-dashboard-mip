# Настройка системы диаграмм
import plotly.express as px
import pandas as pd

def create_bar_chart(df: pd.DataFrame, column_name: str, title: str):
    """Строит столбчатую диаграмму для оценок (например, от 1 до 10)"""
    data = df[column_name].dropna()
    counts = data.value_counts().reset_index()
    counts.columns = ['Оценка', 'Количество']
    counts = counts.sort_values(by='Оценка')
    
    fig = px.bar(
        counts, x='Оценка', y='Количество', 
        title=title, text='Количество',
        color_discrete_sequence=['#4C78A8']
    )
    # Делаем шкалу X дискретной для корректного отображения оценок
    fig.update_xaxes(type='category')
    fig.update_traces(textposition='outside')
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig

def create_donut_chart_from_multiple_cols(df: pd.DataFrame, columns: list, title: str):
    counts = []
    names = []
    
    for col in columns:
        if col in df.columns:
            count = df[col].notna().sum()
            if count > 0:
                counts.append(count)
                # Извлекаем суть ответа после слеша (/)
                name = col.split('/')[-1].strip() if '/' in col else col
                names.append(name)
                
    pie_data = pd.DataFrame({'Вариант': names, 'Голоса': counts})
    fig = px.pie(
        pie_data, names='Вариант', values='Голоса', 
        title=title, hole=0.5
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(showlegend=False, margin=dict(t=40, b=0, l=0, r=0))
    return fig
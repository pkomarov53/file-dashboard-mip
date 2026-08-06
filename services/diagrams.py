# Настройка системы диаграмм
import plotly.express as px
import pandas as pd

def create_bar_chart(df: pd.DataFrame, column_name: str, title: str):
    data = df[column_name].dropna()
    counts = data.value_counts().reset_index()
    counts.columns = ['Оценка', 'Количество']
    counts = counts.sort_values(by='Оценка')
    
    fig = px.bar(
        counts, x='Оценка', y='Количество', 
        title=title, text='Количество',
        color_discrete_sequence=['#4C78A8']
    )

    fig.update_xaxes(type='category')
    fig.update_traces(textposition='outside')
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig

def create_multi_col_chart(df: pd.DataFrame, columns: list, title: str, chart_type: str = "donut"):
    counts = []
    names = []
    
    for col in columns:
        if col in df.columns:
            count = df[col].notna().sum()
            if count > 0:
                counts.append(count)
                name = col.split('/')[-1].strip() if '/' in col else col
                names.append(name)
                
    pie_data = pd.DataFrame({'Вариант': names, 'Голоса': counts})
    if pie_data.empty:
        return None

    if chart_type == "bar":
        # Сортировка по возрастанию для правильного отображения снизу вверх на горизонтальном графике
        pie_data = pie_data.sort_values(by='Голоса', ascending=True)
        fig = px.bar(
            pie_data, 
            x='Голоса', 
            y='Вариант', 
            orientation='h', 
            title=title,
            text='Голоса',
            color_discrete_sequence=['#4C78A8']
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            yaxis_title=None, 
            xaxis_title=None,
            margin=dict(t=40, b=20, l=0, r=20),
            height=max(300, len(pie_data) * 45)
        )
    else:
        # Сортировка по убыванию для кольцевой диаграммы
        pie_data = pie_data.sort_values(by='Голоса', ascending=False)
        fig = px.pie(
            pie_data, 
            names='Вариант', 
            values='Голоса', 
            title=title, 
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(
            textposition='auto', 
            textinfo='percent',
            hovertemplate="<b>%{label}</b><br>Голоса: %{value}<br>Доля: %{percent}<extra></extra>"
        )
        total_votes = pie_data['Голоса'].sum()
        fig.add_annotation(
            text=f"Всего<br><b>{total_votes}</b>", 
            x=0.5, y=0.5, 
            font_size=13, 
            showarrow=False
        )
        fig.update_layout(showlegend=False, margin=dict(t=40, b=20, l=20, r=20))
        
    return fig
# Настройка визуализации данных
import streamlit as st
from services.diagrams import create_bar_chart, create_donut_chart_from_multiple_cols
from services.text_analysis import get_top_words_df, create_wordcloud_fig
import plotly.express as px
import matplotlib.pyplot as plt

def render_dashboard(df):
    st.title("Обратная связь студентов")
        
    # KPI 
    st.markdown("### Сводные показатели")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Всего анкет", len(df))
    
    if 'Насколько Вам был понятен материал модуля?' in df.columns:
        val = df['Насколько Вам был понятен материал модуля?'].mean()
        kpi2.metric("Понятность (ср. балл)", f"{val:.1f} / 10")
        
    if 'Как Вы оцениваете работу спикера модуля?' in df.columns:
        val = df['Как Вы оцениваете работу спикера модуля?'].mean()
        kpi3.metric("Работа спикера (ср. балл)", f"{val:.1f} / 10")
        
    if 'Насколько Вы считаете содержание модуля полезным и важным для вашей практики / целей?' in df.columns:
        val = df['Насколько Вы считаете содержание модуля полезным и важным для вашей практики / целей?'].mean()
        kpi4.metric("Полезность модуля (ср. балл)", f"{val:.1f} / 10")

    st.divider()

    # Вкладки
    tab1, tab2, tab3, tab4 = st.tabs(["Учебный процесс", "Платформа и Наставник", "Карьера и интересы", "Открытые ответы"])

    with tab1:
        st.subheader("Оценка учебных материалов")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = create_bar_chart(df, 'Насколько Вам был понятен материал модуля?', "Понятность материала")
            if fig1: st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = create_bar_chart(df, 'Насколько Вы считаете содержание модуля полезным и важным для вашей практики / целей?', "Полезность для практики")
            if fig2: st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Взаимодействие с платформой")
        col3, col4 = st.columns(2)
        with col3:
            fig3 = create_bar_chart(df, 'Как часто Вы пользуетесь личным кабинетом?', "Частота использования ЛК")
            if fig3: st.plotly_chart(fig3, use_container_width=True)
        with col4:
            mentor_cols = [c for c in df.columns if 'Что Вам больше всего нравится или кажется полезным в учебном канале с наставником?' in c and 'Другое' not in c]
            if mentor_cols:
                fig_mentor = create_donut_chart_from_multiple_cols(df, mentor_cols, "Ценность канала с наставником")
                st.plotly_chart(fig_mentor, use_container_width=True)

    with tab3:
        st.subheader("Профессиональное развитие")
        col5, col6 = st.columns(2)
        with col5:
            direction_cols = [c for c in df.columns if 'Какие направления в психологическом консультировании' in c and 'Другое' not in c]
            if direction_cols:
                fig_dir = create_donut_chart_from_multiple_cols(df, direction_cols, "Интересные направления")
                st.plotly_chart(fig_dir, use_container_width=True)
        with col6:
            career_cols = [c for c in df.columns if 'Что Вы считаете важным в карьере?' in c and 'Другое' not in c]
            if career_cols:
                fig_car = create_donut_chart_from_multiple_cols(df, career_cols, "Важные факторы в карьере")
                st.plotly_chart(fig_car, use_container_width=True)
                
    with tab4:
        st.subheader("Анализ текстовых комментариев")
        st.markdown("Здесь собраны самые часто упоминаемые слова и термины из открытых ответов студентов. Это помогает быстро выявить ключевые запросы на улучшения.")
        
        target_column = 'Что бы Вы хотели изменить или улучшить в этом модуле?'
        
        if target_column in df.columns:
            valid_texts = df[target_column].dropna()
            valid_texts = valid_texts[valid_texts.str.len() > 2]
            
            if not valid_texts.empty:
                col_text1, col_text2 = st.columns([2, 1])
                
                with col_text1:
                    st.markdown("**Облако слов (WordCloud)**")
                    fig_wc = create_wordcloud_fig(valid_texts)
                    if fig_wc:
                        st.pyplot(fig_wc)
                        plt.close(fig_wc)  # освобождение памяти после отрисовки
                
                with col_text2:
                    st.markdown("**Топ-15 частых слов**")
                    top_words_df = get_top_words_df(valid_texts, top_n=15)
                    
                    if not top_words_df.empty:
                        fig_top = px.bar(
                            top_words_df.sort_values('Частота', ascending=True), 
                            x='Частота', 
                            y='Слово', 
                            orientation='h',
                            color_discrete_sequence=['#4C78A8']
                        )
                        fig_top.update_layout(
                            margin=dict(l=0, r=0, t=0, b=0), 
                            height=350,
                            yaxis_title=None,
                            xaxis_title=None
                        )
                        st.plotly_chart(fig_top, use_container_width=True)
            else:
                st.info("Недостаточно текстовых ответов для построения аналитики.")
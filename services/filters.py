# Настройка системы фильтров
import streamlit as st
import pandas as pd

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Настройки фильтрации")
    filtered_df = df.copy()

    # Группа фильтров: Организационные данные
    with st.sidebar.expander("Организационные параметры", expanded=True):
        
        # 1. Фильтр по номеру трека (track_numb)
        if 'track_numb' in filtered_df.columns:
            tracks = filtered_df['track_numb'].dropna().unique().tolist()
            if tracks:
                selected_tracks = st.multiselect("Учебный трек", options=tracks, default=tracks)
                # Оставляем выбранные треки или те строки, где трек не указан
                filtered_df = filtered_df[filtered_df['track_numb'].isin(selected_tracks) | filtered_df['track_numb'].isna()]

        # 2. Фильтр по каналу с наставником
        mentor_col = 'Пользуетесь ли Вы учебным каналом с Наставником?'
        if mentor_col in filtered_df.columns:
            mentor_options = filtered_df[mentor_col].dropna().unique().tolist()
            if mentor_options:
                selected_mentor = st.multiselect("Канал с наставником", options=mentor_options, default=mentor_options)
                filtered_df = filtered_df[filtered_df[mentor_col].isin(selected_mentor) | filtered_df[mentor_col].isna()]

    # Группа фильтров: Оценки и метрики
    with st.sidebar.expander("Оценки студентов", expanded=True):
        
        # 3. Ползунок по оценке работы спикера
        speaker_col = 'Как Вы оцениваете работу спикера модуля?'
        if speaker_col in filtered_df.columns:
            # Преобразуем в числа, игнорируя текстовый мусор
            filtered_df[speaker_col] = pd.to_numeric(filtered_df[speaker_col], errors='coerce')
            
            valid_scores = filtered_df[speaker_col].dropna()
            min_score = int(valid_scores.min()) if not valid_scores.empty else 0
            max_score = int(valid_scores.max()) if not valid_scores.empty else 10
            
            if min_score < max_score:
                selected_score = st.slider(
                    "Оценка спикера", 
                    min_value=min_score, 
                    max_value=max_score, 
                    value=(min_score, max_score)
                )
                filtered_df = filtered_df[
                    (filtered_df[speaker_col] >= selected_score[0]) & 
                    (filtered_df[speaker_col] <= selected_score[1]) | 
                    filtered_df[speaker_col].isna()
                ]

    return filtered_df
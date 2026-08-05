# Настройка системы фильтров
import streamlit as st
import pandas as pd

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Настройки фильтрации")
    
    with st.sidebar.form(key="filters_form"):
        draft_filters = {}

        # --- Группа фильтров: Демография ---
        with st.expander("Демография студентов", expanded=True):
            
            gender_col = 'Укажите Ваш пол'
            if gender_col in df.columns:
                # Добавляем категорию для пустых значений
                genders = df[gender_col].dropna().unique().tolist()
                genders.sort(key=lambda x: str(x))
                
                st.markdown("**Пол**")
                draft_filters['gender'] = [g for g in genders if st.checkbox(str(g), value=True, key=f"f_gender_{g}")]
                
                # Отдельный чекбокс для незаполненных данных
                include_nan = st.checkbox("Не указано (без анкеты)", value=True, key="f_gender_nan")
                draft_filters['gender_include_nan'] = include_nan
                        
            age_col = 'Укажите Ваш возраст'
            if age_col in df.columns:
                ages = df[age_col].dropna().unique().tolist()
                ages.sort(key=lambda x: str(x))
                if ages:
                    st.markdown("**Возраст**")
                    draft_filters['age'] = [a for a in ages if st.checkbox(str(a), value=True, key=f"f_age_{a}")]
                        
            edu_col = 'Имеется ли у вас психологическое образование?'
            if edu_col in df.columns:
                edu_options = df[edu_col].dropna().unique().tolist()
                edu_options.sort(key=lambda x: str(x))
                if edu_options:
                    st.markdown("**Псих. образование**")
                    draft_filters['edu'] = [e for e in edu_options if st.checkbox(str(e), value=True, key=f"f_edu_{e}")]

        # --- Группа фильтров: Организационные параметры ---
        with st.expander("Организационные параметры", expanded=False):
            
            if 'track_numb' in df.columns:
                tracks = df['track_numb'].dropna().unique().tolist()
                tracks.sort(key=lambda x: str(x))
                if tracks:
                    st.markdown("**Учебный трек**")
                    draft_filters['track'] = [t for t in tracks if st.checkbox(str(t), value=True, key=f"f_track_{t}")]

            mentor_col = 'Пользуетесь ли Вы учебным каналом с Наставником?'
            if mentor_col in df.columns:
                mentor_options = df[mentor_col].dropna().unique().tolist()
                mentor_options.sort(key=lambda x: str(x))
                if mentor_options:
                    st.markdown("**Канал с наставником**")
                    draft_filters['mentor'] = [m for m in mentor_options if st.checkbox(str(m), value=True, key=f"f_mentor_{m}")]

        # --- Группа фильтров: Оценки ---
        with st.expander("Оценки студентов", expanded=False):
            
            speaker_col = 'Как Вы оцениваете работу спикера модуля?'
            if speaker_col in df.columns:
                valid_scores = pd.to_numeric(df[speaker_col], errors='coerce').dropna()
                
                if not valid_scores.empty:
                    min_score = int(valid_scores.min())
                    max_score = int(valid_scores.max())
                    if min_score < max_score:
                        draft_filters['speaker_score'] = st.slider(
                            "Оценка спикера", 
                            min_value=min_score, max_value=max_score, value=(min_score, max_score)
                        )
                    else:
                        draft_filters['speaker_score'] = (min_score, max_score)
                else:
                    draft_filters['speaker_score'] = None

        submit_button = st.form_submit_button(label="Применить фильтрацию", type="primary", use_container_width=True)

    if 'applied_filters' not in st.session_state:
        st.session_state['applied_filters'] = draft_filters

    if submit_button:
        st.session_state['applied_filters'] = draft_filters

    # --- ФИЛЬТРАЦИЯ ДАТАФРЕЙМА ---
    filtered_df = df.copy()
    applied = st.session_state['applied_filters']

    if 'gender' in applied and gender_col in filtered_df.columns:
        selected_genders = applied['gender']
        include_nan = applied.get('gender_include_nan', True)
        
        gender_mask = filtered_df[gender_col].isin(selected_genders)
        if include_nan:
            gender_mask |= filtered_df[gender_col].isna()
            
        filtered_df = filtered_df[gender_mask]
        
    if applied.get('age') and age_col in filtered_df.columns:
        all_ages = df[age_col].dropna().unique().tolist()
        if len(applied['age']) < len(all_ages):
            filtered_df = filtered_df[filtered_df[age_col].isin(applied['age'])]
        
    if applied.get('edu') and edu_col in filtered_df.columns:
        all_edus = df[edu_col].dropna().unique().tolist()
        if len(applied['edu']) < len(all_edus):
            filtered_df = filtered_df[filtered_df[edu_col].isin(applied['edu'])]
        
    if applied.get('track') and 'track_numb' in filtered_df.columns:
        all_tracks = df['track_numb'].dropna().unique().tolist()
        if len(applied['track']) < len(all_tracks):
            filtered_df = filtered_df[filtered_df['track_numb'].isin(applied['track'])]
        
    if applied.get('mentor') and mentor_col in filtered_df.columns:
        all_mentors = df[mentor_col].dropna().unique().tolist()
        if len(applied['mentor']) < len(all_mentors):
            filtered_df = filtered_df[filtered_df[mentor_col].isin(applied['mentor'])]
        
    if applied.get('speaker_score') and speaker_col in filtered_df.columns:
        score_min, score_max = applied['speaker_score']
        speaker_series = pd.to_numeric(filtered_df[speaker_col], errors='coerce')
        
        in_range_mask = speaker_series.between(score_min, score_max)
        isna_mask = speaker_series.isna()
        
        filtered_df = filtered_df[in_range_mask | isna_mask]

    return filtered_df
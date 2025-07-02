import streamlit as st
from heroes.main_functions import is_win, format_duration, calculate_kda
from heroes.special_functions import get_contribution_label
from heroes.chart import plot_kda_stats
from datetime import datetime
from heroes.main_function import fetch_matches

def hero_analysis_page():
    st.title("📊 Анализ героев в Dota 2")

    with st.sidebar:
        hero_id = st.number_input("Введите Hero ID", min_value=1, value=1)
        match_count = st.slider("Количество матчей", 10, 50, 100)
        run = st.button("🔍 Проанализировать")

    if run:
        matches = fetch_matches(hero_id, match_count)

        if not matches:
            st.error("❌ Не удалось получить данные")
            return

        st.session_state["heroes"] = matches
        st.session_state["hero_id"] = hero_id

    if "heroes" in st.session_state and "hero_id" in st.session_state:
        st.write("Данные есть, можно строить график")

        matches = st.session_state["heroes"]
        hero_id = st.session_state["hero_id"]

        st.subheader(f"Результаты анализа (Hero ID: {hero_id})")

        for match in matches:
            k, d, a = match["kills"], match["deaths"], match["assists"]
            kda = calculate_kda(k, d, a)
            label = get_contribution_label(k, d, a)
            result = "✅ Победа" if is_win(match) else "❌ Поражение"
            duration = format_duration(match['duration'])
            kills = match['kills']
            deaths = match['deaths']
            assists = match['assists']
            start_time = datetime.fromtimestamp(match["start_time"]).strftime("%d.%m.%Y %H:%M")

            st.markdown(f"""
               ### 🕹️ Матч `{match['match_id']}`
               - **Результат**: {result}  
               - **Время**: `{duration}`
               - **Дата игры: {start_time}**
               - **Убийства**: {kills}  
               - **Смерти**: {deaths}  
               - **Помощи**: {assists}  
               - **KDA**: `{k}/{d}/{a}` → **{kda:.2f}**  
               - **Оценка вклада**: {label}  
               ---
               """)

        if st.button("📈 Построить граф-отчёт"):
            plot_kda_stats(matches, hero_id)


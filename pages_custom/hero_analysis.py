import streamlit as st
from heroes.main_functions import is_win, format_duration, calculate_kda
from heroes.special_functions import get_contribution_label
from heroes.chart import plot_kda_stats
from datetime import datetime
from heroes.main_function import fetch_hero_by_match
import json

with open("data/heroes.json", encoding="utf-8") as f:
    heroes = json.load(f)

hero_name_to_id = {name: int(id_) for id_, name in heroes.items()}
hero_id_to_name = {int(id_): name for id_, name in heroes.items()}


def hero_analysis_page():
    st.title("📊 Анализ героев в Dota 2")

    with st.sidebar:
        search_mode = st.radio("Как выбрать героя?", ["По ID", "По имени"])

        if search_mode == "По ID":
            hero_id = st.number_input("Введите Hero ID", min_value=1, value=1)
        else:
            hero_name = st.selectbox("Выберите героя", sorted(hero_name_to_id.keys()))
            hero_id = hero_name_to_id[hero_name]

        match_count = st.slider("Количество матчей", 10, 50, 100)
        run = st.button("🔍 Проанализировать")

    if run:
        matches = fetch_hero_by_match(hero_id, match_count)

        if not matches:
            st.error("❌ Не удалось получить данные")
            return

        st.session_state["heroes"] = matches
        st.session_state["hero_id"] = hero_id

    if "heroes" in st.session_state and "hero_id" in st.session_state:
        st.write("Данные есть, можно строить график")

        matches = st.session_state["heroes"]
        hero_id = st.session_state["hero_id"]
        hero_name = hero_id_to_name.get(hero_id, f"ID: {hero_id}")

        st.subheader(f"Результаты анализа героя: {hero_name}")

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


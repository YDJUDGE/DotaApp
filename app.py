import streamlit as st
import requests
from matches.main_functions import is_win, format_duration, calculate_kda
from matches.special_functions import get_contribution_label
from matches.chart import plot_kda_stats
from datetime import datetime


def fetch_matches(hero_id: int, limit=10):
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matches"
    data = requests.get(url)
    return data.json()[:limit] if data.status_code == 200 else []


def app():
    st.set_page_config(page_title="Dota 2 Анализ", layout="wide")
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

        st.session_state["matches"] = matches
        st.session_state["hero_id"] = hero_id

    if "matches" in st.session_state and "hero_id" in st.session_state:
        st.write("Данные есть, можно строить график")

        matches = st.session_state["matches"]
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

if __name__ == "__main__":
    app()

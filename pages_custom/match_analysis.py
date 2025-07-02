import streamlit as st
from heroes.main_functions import calculate_kda, format_duration
from matches.main_function import fetch_match_by_id
from matches.main_functions import format_items
from matches.main_functions import get_hero_by_id
from heroes.special_functions import get_contribution_label


def match_details_page():
    st.title("🧩 Анализ определённого матча в Dota 2")

    with st.sidebar:
        match_id = st.number_input("Введите Match ID", min_value=1)
        run = st.button("🔍 Проанализировать")

    if run:
        match_data = fetch_match_by_id(match_id)

        if not match_data:
            st.error("❌ Не удалось получить данные по матчу")
            return

        st.session_state['match'] = match_data

    if "match" in st.session_state:
        match_data = st.session_state['match']
        st.subheader("🧾 Общая информация о матче")

        match_data = st.session_state["match"]
        duration = format_duration(match_data.get("duration"))
        radiant_win = match_data.get("radiant_win")
        radiant_score = match_data.get("radiant_score")
        dire_score = match_data.get("dire_score")
        first_blood = format_duration(match_data.get("first_blood_time"))
        result = "Силы Света ✅" if radiant_win else "Силы Тьмы ✅"

        st.markdown(f"""
        - **Победитель**: {result}
        - **Длительность**: '{duration}'
        - **Счёт(Силы Света:Силы Тьмы)**: {radiant_score} : {dire_score}
        - **Первая Кровь**: {first_blood}
        ---
        """)

        st.subheader("🧑 Игроки")

        players = match_data.get("players", [])

        for player in players:
            name = player.get('personaname', 'Аноним')
            is_radiant = player.get("isRadiant")
            team = "Силы Света" if is_radiant else "Силы Тьмы"

            k, d, a = player.get('kills', 0), player.get('deaths', 0), player.get('assists', 0)
            kda = calculate_kda(k, d, a)
            items = format_items([
                player.get("item_0"), player.get("item_1"), player.get("item_2"),
                player.get("item_3"), player.get("item_4"), player.get("item_5"),
            ])

            st.markdown(f"""
            #### 🎮 {name} ({team})
            - **Герой**: {get_hero_by_id(player.get("hero_id"))}
            - **Убийства / Смерти / Помощи**: `{k}/{d}/{a}`  
            - **KDA**: **{kda:.2f}**  
            - **GPM / XPM**: `{player.get("gold_per_min")}` / `{player.get("xp_per_min")}`
            - **Ластхиты / Денай**: `{player.get("last_hits")}` / `{player.get("denies")}`  
            - **Урон по героям / по башням / лечение**: `{player.get("hero_damage")}` / `{player.get("tower_damage")}` / `{player.get("hero_healing")}`  
            - **Предметы**: {", ".join(items)}
            - **Общая оценка**: {get_contribution_label(k, d, a)}
            ---
            """)

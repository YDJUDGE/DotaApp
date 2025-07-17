import streamlit as st
from pro_players.main_functions import analyze_pro_player


def pro_player_analysis_page():
    st.title("🌟 Анализ ПРО-игрока Dota 2")
    st.warning("⚠️ Эта страница предназначена только для анализа **про-игроков**. "
               "Для обычных игроков используйте другой раздел.")

    account_id = st.text_input("Введите Steam ID (число):")
    run = st.button("🔍 Проанализировать")

    if run and account_id:
        try:
            account_id_int = int(account_id)
        except ValueError:
            st.error("Введите корректный числовой Steam ID")
            return

        with st.spinner("Анализируем игрока..."):
            result, error = analyze_pro_player(account_id_int)

        if error:
            st.error(error)
            return

        st.markdown(f"""
        ## 📊 Результаты анализа про-игрока (Steam ID: {result['account_id']})

        - **Skill Score:** {result['skill_score']}
        - **Звание:** {result['rank_name']}
        - **MMR:** {result['mmr_text']}
        - **Роли (играет):** {', '.join(result['roles']) if result['roles'] else 'Не определено'}
        - **Модификатор роли:** {result['role_modifier']}
        - **Бонус универсальности:** {result['versatility_bonus']}
        - **Тип игрока:** {result['player_class']}
        - **Рекомендуемая трансферная стоимость:** ${result['transfer_price']:,.2f}
        - **Ориентировочная месячная зарплата:** ${result['salary']:,.2f}
        """)

        st.markdown("### 🏆 Топ-5 часто используемых героев:")
        for i, hero_info in enumerate(result["top_heroes"], 1):
            hero_name = hero_info['hero_name']
            count = hero_info['count']
            winrate = hero_info['winrate']
            st.markdown(f"**{i}.** Герой: **{hero_name}** — использован {count} раз — винрейт {winrate:.1f}%")

        st.info("📌 Анализ основан на последних 100 матчах.")
        st.info(
            "⚠️ Внимание: из-за ограничений API и фильтров в выборку могут попасть не все матчи игрока, результаты анализа — приближённые.")

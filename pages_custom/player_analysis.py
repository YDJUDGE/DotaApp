import streamlit as st
from players.main_function import fetch_last_matches_detailed, fetch_player_profile
from players.main_functions import calculate_skill_score, get_roles_from_matches, calculate_transfer_price
from players.classification import classify_player, calculate_role_modifier

def player_analysis_page():
    st.title("💎 Анализ игрока Dota 2 и оценка трансферной стоимости")

    account_id = st.text_input("Введите Steam Account ID (число):")
    run = st.button("🔍 Проанализировать")

    if run and account_id:
        try:
            account_id_int = int(account_id)
        except ValueError:
            st.error("Введите корректный числовой Account ID")
            return

        with st.spinner("🧠 Анализируем игрока. Считаем стоимость, Это заёмет несколько минут"):
            profile = fetch_player_profile(account_id_int)
            matches = fetch_last_matches_detailed(account_id_int)

        if not matches or len(matches) < 10:
            st.error("Не удалось получить матчи или их слишком мало")
            return

        mmr = profile.get("real_mmr_score", 0)

        if mmr >= 3000:
            mmr_text = str(mmr)
            mmr_for_calc = mmr
        elif mmr > 0:
            mmr_text = "ниже 3000"
            mmr_for_calc = 0
        else:
            mmr_text = "не определён"
            mmr_for_calc = 0

        skill_score = calculate_skill_score(matches)
        skill_score = max(skill_score, 0)
        roles = get_roles_from_matches(matches)
        role_modifier, versatility_bonus = calculate_role_modifier(roles)

        behavior_coeff = 1.0  # Пока заглушка
        media_score = 5  # Пока заглушка

        transfer_price = calculate_transfer_price(
            skill_score,
            mmr_for_calc,
            media_score,
            role_modifier,
            behavior_coeff,
            versatility_bonus
        )

        player_class = classify_player(matches)

        st.markdown(f"""
            ## Результаты анализа для аккаунта {account_id}

            - **Skill Score:** {skill_score}
            - **MMR:** {mmr_text}
            - **Роли (играет):** {', '.join(roles) if roles else 'Не определено'}
            - **Модификатор роли:** {role_modifier}
            - **Бонус универсальности:** {versatility_bonus}
            - **Тип игрока:** {player_class}
            - **Рекомендуемая трансферная стоимость:** ${transfer_price}
            """)



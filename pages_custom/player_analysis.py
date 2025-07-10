import streamlit as st
from players.main_function import fetch_last_matches_detailed, fetch_player_profile
from players.main_functions import calculate_skill_score, get_roles_from_matches, calculate_transfer_price, \
    load_rank_mapping
from players.classification import normalize_roles_for_modifier, calculate_role_modifier, classify_player

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
            rank_mapping = load_rank_mapping()

            rank_tier = profile.get("rank_tier", 0)
            rank_info = rank_mapping.get(str(rank_tier), {"name": "неизвестно", "mmr": 0})
            rank_name = rank_info["name"]
            estimated_mmr = rank_info["mmr"]


        if not matches or len(matches) < 10:
            st.error("Не удалось получить матчи или их слишком мало")
            return

        real_mmr = profile.get("real_mmr_score", 0)

        if real_mmr >= 3000:
            mmr_text = str(real_mmr)
            mmr_for_calc = real_mmr
        elif real_mmr > 0:
            mmr_text = "ниже 3000"
            mmr_for_calc = 0
        elif estimated_mmr > 0:
            mmr_text = f"~{estimated_mmr} (по рангу: {rank_name})"
            mmr_for_calc = estimated_mmr
        else:
            mmr_text = "не определён"
            mmr_for_calc = 0

        skill_score = calculate_skill_score(matches)
        skill_score = max(skill_score, 0)
        roles = get_roles_from_matches(matches)
        normalized_roles = normalize_roles_for_modifier(roles)
        role_modifier, versatility_bonus = calculate_role_modifier(normalized_roles)
        player_class = classify_player(matches)

        behavior_coeff = 1.0  # Пока заглушка
        media_score = 3  # Пока заглушка

        transfer_price = calculate_transfer_price(
            skill_score,
            mmr_for_calc,
            media_score,
            role_modifier,
            behavior_coeff,
            versatility_bonus
        )


        st.markdown(f"""
            ## Результаты анализа для аккаунта {account_id}

            - **Skill Score:** {skill_score}
            - **Звание:** {rank_name}
            - **MMR:** {mmr_text}
            - **Роли (играет):** {', '.join(roles) if roles else 'Не определено'}
            - **Модификатор роли:** {role_modifier}
            - **Бонус универсальности:** {versatility_bonus}
            - **Тип игрока:** {player_class}
            - **Рекомендуемая трансферная стоимость:** ${transfer_price}
            """)



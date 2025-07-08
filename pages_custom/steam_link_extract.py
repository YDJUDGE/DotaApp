import streamlit as st
from resolve.main_function_extract import extract_steam64, steam64_to_steam32

def steamid_resolver_page():
    st.title("🔎 Steam → Steam32 ID")

    st.markdown("""
    Введите **ссылку** на профиль или Steam64 ID (17 цифр).  
    Например: `https://steamcommunity.com/profiles/76561198015403682` или просто `76561198015403682`.
    """)

    input_id = st.text_input("Ваш Steam ID или ссылка на профиль:")

    if st.button("Преобразовать") and input_id:
        steam64 = extract_steam64(input_id.strip())
        if steam64:
            steam32 = steam64_to_steam32(steam64)
            st.success(f"🎯 Найден Steam32 ID: `{steam32}`")
        else:
            st.error("❌ Не удалось определить Steam ID. Вводите только ссылку на профиль (с `/profiles/`) или Steam64 ID.")

    # Пояснение
    st.markdown("""
    ---
    ### ❗ Как правильно ввести Steam ID?

    Для корректной работы анализа, **нужен числовой Steam ID** (SteamID64), например:

    ✅ Подходят такие варианты:
    - `https://steamcommunity.com/profiles/76561198015403682`
    - `76561198015403682`

    🚫 Не подходят:
    - `https://steamcommunity.com/id/dendi`
    - `dendi`

    <span style='color: gray; font-size: 0.9em;'>Мы не используем Steam API Key, поэтому <u>кастомные имена (доменные)</u> не поддерживаются.</span>
    """, unsafe_allow_html=True)

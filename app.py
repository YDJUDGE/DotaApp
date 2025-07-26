import streamlit as st
from pages_custom.hero_analysis import hero_analysis_page
from pages_custom.match_analysis import match_details_page
from pages_custom.player_analysis import player_analysis_page
from pages_custom.steam_link_extract import steamid_resolver_page
from pages_custom.pro_player_analysis import pro_player_analysis_page
from pages_custom.faq_page import faq_page

def app():
    st.set_page_config(page_title="Dota 2 Анализ", layout="wide")

    # Навигация по "страницам"
    with st.sidebar:
        st.title("Меню")
        page = st.selectbox("Выберите раздел", [
            "Анализ героев",
            "Анализ конкретного матча",
            "Анализ игрока и его оценка",
            "Получить Steam32",
            "Анализ про-игрока",
            "FAQ"
        ])

    # Отображение выбранной страницы
    if page == "Анализ героев":
        hero_analysis_page()
    elif page == "Анализ конкретного матча":
        match_details_page()
    elif page == "Анализ игрока и его оценка":
        player_analysis_page()
    elif page == "Анализ про-игрока":
        pro_player_analysis_page()
    elif page == "Получить Steam32":
        steamid_resolver_page()
    elif page == "FAQ":
        faq_page()

if __name__ == "__main__":
    app()

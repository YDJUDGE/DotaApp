import streamlit as st
from heroes.main_functions import is_win, format_duration, calculate_kda
from heroes.special_functions import get_contribution_label
from heroes.chart import plot_kda_stats
from datetime import datetime
from heroes.main_function import fetch_matches
from pages.hero_analysis import hero_analysis_page
from pages.match_details import match_details_page

def app():
    st.set_page_config(page_title="Dota 2 Анализ", layout="wide")

    # Навигация по "страницам"
    with st.sidebar:
        st.title("Меню")
        page = st.selectbox("Выберите раздел", [
            "Анализ героев",
            "Анализ конкретного матча"
        ])

    # Отображение выбранной страницы
    if page == "Анализ героев":
        hero_analysis_page()
    elif page == "Анализ конкретного матча":
        match_details_page()

if __name__ == "__main__":
    app()

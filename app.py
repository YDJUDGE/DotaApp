import streamlit as st
from pages_custom.hero_analysis import hero_analysis_page
from pages_custom.match_analysis import match_details_page

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

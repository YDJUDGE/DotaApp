import matplotlib.pyplot as plt
import streamlit as st
from heroes.main_functions import calculate_kda
from heroes.special_functions import get_contribution_label


def plot_kda_stats(matches, hero_id):
    match_ids = []
    kdas = []
    labels = []
    colors = []

    color_map = {
        "MVP 🏆": "gold",
        "Игра зависела от него": "red",
        "Хороший вклад в игру": "green",
        "Средний вклад в игру": "orange",
        "Слабое звено ❌": "gray"
    }

    for match in matches:
        k = match['kills']
        d = match['deaths']
        a = match['assists']
        kda = calculate_kda(k, d, a)
        label = get_contribution_label(k, d, a)

        match_ids.append(str(match['match_id']))
        kdas.append(kda)
        labels.append(label)
        colors.append(color_map.get(label, "blue"))

    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(match_ids, kdas, c=colors, s=100, edgecolors='black')

    ax.set_title(f"KDA анализ по матчам (Герой ID: {hero_id})")
    ax.set_xlabel("Match ID")
    ax.set_ylabel("KDA")
    plt.xticks(rotation=45)
    ax.grid(True)
    fig.tight_layout()

    st.pyplot(fig)

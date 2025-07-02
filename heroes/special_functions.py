from heroes.main_functions import calculate_kda

def get_contribution_label(kills, deaths, assists):
    kda = calculate_kda(kills, deaths, assists)

    if deaths in (0, 1) and kills > 14 and assists > 5:
        return "MVP 🏆"
    elif kda >=25:
        return "MVP 🏆"
    elif kda > 7:
        return "Игра зависела от него"
    elif kda >= 4:
        return "Хороший вклад в игру"
    elif kda >= 2:
        return "Средний вклад в игру"
    else:
        return "Слабое звено ❌"


import requests
from dotenv import load_dotenv
from heroes.main_functions import is_win, format_duration, calculate_kda
from heroes.special_functions import get_contribution_label
from heroes.chart import plot_kda_stats

load_dotenv()

def fetch_matches(hero_id: int, limit=10):
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matches"
    data = requests.get(url)
    return data.json()[:limit] if data.status_code == 200 else "Ошибка сервера"

def main():
    try:
        hero_id = int(input("Введите ID героя: "))
        match_count = int(input("Сколько матчей анализировать? "))

    except ValueError:
        print("Введите корректные числа")
        return

    matches = fetch_matches(hero_id, match_count)

    if not matches:
        print("Матчи не найдены или ошибка сервера.")
        return

    for match in matches:
        win = "Победа" if is_win(match) else "Поражение"
        duration = format_duration(match['duration'])
        kda = calculate_kda(match['kills'], match['deaths'], match['assists'])
        label = get_contribution_label(match['kills'], match['deaths'], match['assists'])

        info = (
            f"ID матча: {match['match_id']}\n"
            f"{win}\n"
            f"Время: {duration}\n"
            f"Убийства: {match['kills']}\n"
            f"Смерти: {match['deaths']}\n"
            f"Помощи: {match['assists']}\n"
            f"КПД: {kda:.2f}\n"
            f"Оценка игрока: {label}\n"
        )

        print(info)

    plot_kda_stats(matches, hero_id)

if __name__ == "__main__":
    main()

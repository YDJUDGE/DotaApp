import requests
import json
import os

def fetch_and_save_heroes():
    url = "https://api.opendota.com/api/heroes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hero_mapping = {hero["id"]: hero["localized_name"] for hero in data}

        os.makedirs("data", exist_ok=True)
        with open("data/heroes.json", "w", encoding="utf-8") as f:
            json.dump(hero_mapping, f, ensure_ascii=False, indent=4)

        print("✅ Герои успешно сохранены в match/data/heroes.json")
    else:
        print(f"❌ Ошибка: {response.status_code}")

if __name__ == "__main__":
    fetch_and_save_heroes()

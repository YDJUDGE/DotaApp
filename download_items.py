# download_items.py
import requests
import json
import os

def fetch_and_save_items():
    url = "https://api.opendota.com/api/constants/items"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        item_mapping = {}

        for item_name, item_data in data.items():
            item_id = item_data.get("id")
            localized_name = item_data.get("dname") or item_name
            if item_id is not None:
                item_mapping[item_id] = localized_name

        os.makedirs("data", exist_ok=True)
        with open("data/items.json", "w", encoding="utf-8") as f:
            json.dump(item_mapping, f, ensure_ascii=False, indent=4)

        print("✅ Предметы успешно сохранены в match/data/items.json")
    else:
        print(f"❌ Ошибка: {response.status_code}")

if __name__ == "__main__":
    fetch_and_save_items()

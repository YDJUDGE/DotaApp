import json
import os

def fetch_and_save_ranks():
    raw_rank_mapping = {
        "11": "Herald I", "12": "Herald II", "13": "Herald III", "14": "Herald IV", "15": "Herald V",
        "21": "Guardian I", "22": "Guardian II", "23": "Guardian III", "24": "Guardian IV", "25": "Guardian V",
        "31": "Crusader I", "32": "Crusader II", "33": "Crusader III", "34": "Crusader IV", "35": "Crusader V",
        "41": "Archon I", "42": "Archon II", "43": "Archon III", "44": "Archon IV", "45": "Archon V",
        "51": "Legend I", "52": "Legend II", "53": "Legend III", "54": "Legend IV", "55": "Legend V",
        "61": "Ancient I", "62": "Ancient II", "63": "Ancient III", "64": "Ancient IV", "65": "Ancient V",
        "71": "Divine I", "72": "Divine II", "73": "Divine III", "74": "Divine IV", "75": "Divine V",
        "80": "Immortal",
        "0": "Неизвестен"
    }

    # Примерная шкала MMR по рангу
    mmr_mapping = {
        "11": 800, "12": 1000, "13": 1100, "14": 1200, "15": 1300,
        "21": 1400, "22": 1500, "23": 1600, "24": 1700, "25": 1800,
        "31": 1900, "32": 2000, "33": 2100, "34": 2200, "35": 2300,
        "41": 2400, "42": 2500, "43": 2600, "44": 2700, "45": 2800,
        "51": 2900, "52": 3000, "53": 3100, "54": 3200, "55": 3300,
        "61": 3400, "62": 3600, "63": 3800, "64": 4000, "65": 4200,
        "71": 4400, "72": 4600, "73": 4800, "74": 5000, "75": 5200,
        "80": 6000,
        "0": 0
    }

    # Комбинируем всё в новый формат
    full_mapping = {
        rank_id: {
            "name": raw_rank_mapping[rank_id],
            "mmr": mmr_mapping.get(rank_id, 0)
        }
        for rank_id in raw_rank_mapping
    }

    os.makedirs("data", exist_ok=True)
    with open("data/ranks.json", "w", encoding="utf-8") as f:
        json.dump(full_mapping, f, ensure_ascii=False, indent=4)

    print("✅ Ранги успешно сохранены в data/ranks.json")

if __name__ == "__main__":
    fetch_and_save_ranks()

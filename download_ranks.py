import json
import os

def fetch_and_save_ranks():
    rank_mapping = {
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

    os.makedirs("data", exist_ok=True)
    with open("data/ranks.json", "w", encoding="utf-8") as f:
        json.dump(rank_mapping, f, ensure_ascii=False, indent=4)

    print("✅ Ранги успешно сохранены в data/ranks.json")

if __name__ == "__main__":
    fetch_and_save_ranks()
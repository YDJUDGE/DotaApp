import requests

import requests
import time

def fetch_last_matches_detailed(account_id, limit=50):
    base_url = f"https://api.opendota.com/api/players/{account_id}/matches?limit={limit}"
    response = requests.get(base_url)
    if response.status_code != 200:
        return []

    basic_matches = response.json()
    detailed_matches = []

    for match in basic_matches:
        match_id = match.get("match_id")
        if not match_id:
            continue

        match_url = f"https://api.opendota.com/api/matches/{match_id}"
        match_resp = requests.get(match_url)

        if match_resp.status_code != 200:
            continue

        full_match = match_resp.json()

        # Найдём игрока с нужным account_id
        player_data = next((p for p in full_match.get("players", []) if p.get("account_id") == account_id), None)
        if player_data:
            # Добавим поле match_id для дальнейшей обработки
            player_data["match_id"] = match_id
            detailed_matches.append(player_data)

        # Пауза, чтобы не перегрузить API (ограничение ~60 запросов/минуту)
        time.sleep(1)

    return detailed_matches



def fetch_player_profile(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        profile = response.json()
        mmr_estimate = profile.get("mmr_estimate", {}).get("estimate", 0)
        profile["real_mmr_score"] = mmr_estimate
        return profile
    return {}

def fetch_player_rank(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}/ratings"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        rank_tier = response.json()[0].get("rank_tier", 0)
        return rank_tier
    return 0


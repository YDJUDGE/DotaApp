import requests
import time

ALLOWED_GAME_MODES = {1, 2, 3, 4, 5, 16, 17, 22}

ALLOWED_LOBBY_TYPES = {0, 2, 5, 6, 7, 9}

def fetch_last_matches_detailed(account_id, limit=100):
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

        game_mode = full_match.get("game_mode")
        lobby_type = full_match.get("lobby_type")

        if game_mode in ALLOWED_GAME_MODES and lobby_type in ALLOWED_LOBBY_TYPES:
            # Найдём игрока с нужным account_id
            player_data = next((p for p in full_match.get("players", []) if p.get("account_id") == account_id), None)
            if player_data:
                player_data["match_id"] = match_id
                detailed_matches.append(player_data)

        time.sleep(0.05)

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


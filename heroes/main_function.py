import requests

def fetch_hero_by_match(hero_id: int, limit=10):
    url = f"https://api.opendota.com/api/heroes/{hero_id}/matches"
    data = requests.get(url)
    return data.json()[:limit] if data.status_code == 200 else []


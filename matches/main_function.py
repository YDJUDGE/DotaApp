import requests

def fetch_match_by_id(match_id: int):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    data = requests.get(url)
    return data.json() if data.status_code == 200 else []

import aiohttp
import asyncio

MAX_CONCURRENT_REQUESTS = 10
ALLOWED_GAME_MODES = {2}
ALLOWED_LOBBY_TYPES = {7}
API_KEY = ""

async def fetch_match_details(session, match_id, account_id, semaphore, retries=3):
    """Получение деталей матча с учётом лимитов API."""
    url = f"https://api.opendota.com/api/matches/{match_id}"
    params = {"api_key": API_KEY} if API_KEY else {}
    async with semaphore:
        for attempt in range(retries + 1):
            try:
                async with session.get(url, params=params) as resp:
                    if resp.status == 429:
                        retry_after = resp.headers.get('Retry-After')
                        wait_time = float(retry_after) if retry_after else (2 ** attempt) + 3
                        if attempt < retries:
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            return None
                    if resp.status != 200:
                        return None

                    match = await resp.json()
                    if (match.get("lobby_type") not in ALLOWED_LOBBY_TYPES
                            and match.get("game_mode") not in ALLOWED_GAME_MODES):
                        return None

                    player_data = next((p for p in match.get("players", []) if p.get("account_id") == account_id), None)
                    if not player_data:
                        return None

                    player_data["match_id"] = match_id
                    return player_data

            except Exception:
                return None

async def fetch_last_pro_matches_for_player(account_id, limit=100):
    """Получение последних pro-матчей игрока с оптимизацией запросов."""
    url = f"https://api.opendota.com/api/players/{account_id}/matches"
    params = {"limit": limit, "api_key": API_KEY} if API_KEY else {"limit": limit}
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as resp:
                if resp.status == 429:
                    retry_after = resp.headers.get('Retry-After')
                    wait_time = float(retry_after) if retry_after else 10
                    await asyncio.sleep(wait_time)
                    async with session.get(url, params=params) as resp_retry:
                        if resp_retry.status != 200:
                            return []
                        base_matches = await resp_retry.json()
                elif resp.status != 200:
                    return []
                else:
                    base_matches = await resp.json()
        except Exception:
            return []

        pro_and_captains_matches = [
            m for m in base_matches if
            m.get("lobby_type") in ALLOWED_LOBBY_TYPES or m.get("game_mode") in ALLOWED_GAME_MODES
        ]

        if not pro_and_captains_matches:
            return []

        batch_size = 10
        detailed_matches = []
        rate_limit_delay = 0.6

        for i in range(0, len(pro_and_captains_matches), batch_size):
            batch = pro_and_captains_matches[i:i + batch_size]
            tasks = [
                fetch_match_details(session, m["match_id"], account_id, semaphore)
                for m in batch if m.get("match_id")
            ]
            results = await asyncio.gather(*tasks)
            successful = [r for r in results if r]
            detailed_matches.extend(successful)

            await asyncio.sleep(len(batch) * rate_limit_delay)

        return detailed_matches

async def get_pro_player_team(account_id):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.opendota.com/api/proPlayers", params={"api_key": API_KEY} if API_KEY else {}) as response:
            if response.status == 200:
                players = await response.json()
                for p in players:
                    if p["account_id"] == account_id:
                        return p.get("team_name", "Неизвестно\Нет")
                return "Неизвестно"
            return "Неизвестно"

async def fetch_player_profile(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    params = {"api_key": API_KEY} if API_KEY else {}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception:
        return None
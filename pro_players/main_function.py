import aiohttp
import asyncio
import requests

MAX_CONCURRENT_REQUESTS = 5
ALLOWED_GAME_MODES = {2}
ALLOWED_LOBBY_TYPES = {7}
RETRY_DELAY = 3  # секунды для повтора при 429

async def fetch_match_details(session, match_id, account_id, semaphore, retries=3):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    async with semaphore:
        for attempt in range(retries):
            try:
                async with session.get(url) as resp:
                    if resp.status == 429:
                        print(f"[RETRY] Match {match_id} - 429 Too Many Requests. Delay {RETRY_DELAY}s")
                        await asyncio.sleep(RETRY_DELAY)
                        continue
                    if resp.status != 200:
                        print(f"[WARN] Failed to fetch match {match_id}, status: {resp.status}")
                        return None

                    match = await resp.json()
                    player_data = next((p for p in match.get("players", []) if p.get("account_id") == account_id), None)
                    if not player_data:
                        print(f"[INFO] Player {account_id} not found in match {match_id}")
                        return None

                    player_data["match_id"] = match_id
                    print(f"[OK] Found player in match {match_id}")
                    return player_data
            except Exception as e:
                print(f"[ERROR] Exception while fetching match {match_id}: {e}")
                return None
        print(f"[FAIL] Match {match_id} failed after {retries} retries")
        return None


def get_pro_player_team(account_id):
    response = requests.get("https://api.opendota.com/api/proPlayers")
    if response.status_code == 200:
        players = response.json()
        for p in players:
            if p["account_id"] == account_id:
                return p.get("team_name", "Неизвестно")
    return "Неизвестно"


async def fetch_last_pro_matches_for_player(account_id, limit=100):
    url = f"https://api.opendota.com/api/players/{account_id}/matches"
    params = {"limit": limit}

    print(f"[DEBUG] Запрашиваем последние {limit} матчей игрока {account_id}")
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                print(f"[ERROR] Can't fetch base matches list: {resp.status}")
                return []

            base_matches = await resp.json()
            print(f"[DEBUG] Получено {len(base_matches)} матчей (всего)")

        pro_and_captains_matches = [
            m for m in base_matches if m.get("lobby_type") in ALLOWED_LOBBY_TYPES or m.get("game_mode") in ALLOWED_GAME_MODES
        ]

        print(f"[DEBUG] Отфильтровано pro матчей: {len(pro_and_captains_matches)}")

        if not pro_and_captains_matches:
            print(f"[WARN] Нет pro матчей у игрока {account_id}")
            return []

        batch_size = 5  # меньше батчей = меньше шансов на 429
        detailed_matches = []

        for i in range(0, len(pro_and_captains_matches), batch_size):
            batch = pro_and_captains_matches[i:i + batch_size]
            print(f"[DEBUG] Загружаем детали матчей: {[m['match_id'] for m in batch]}")
            tasks = [
                fetch_match_details(session, m["match_id"], account_id, semaphore)
                for m in batch if m.get("match_id")
            ]
            results = await asyncio.gather(*tasks)
            successful = [r for r in results if r]
            print(f"[DEBUG] Успешно загружено матчей: {len(successful)}")
            detailed_matches.extend(successful)

            await asyncio.sleep(2.5)  # важно! реже бить в API

        print(f"[DEBUG] Всего загружено подробных pro матчей: {len(detailed_matches)}")
        return detailed_matches


async def fetch_player_profile_async(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


def fetch_player_profile(account_id):
    return asyncio.run(fetch_player_profile_async(account_id))

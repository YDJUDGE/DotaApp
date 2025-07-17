import aiohttp
import asyncio
import requests

MAX_CONCURRENT_REQUESTS = 5

async def fetch_match_details(session, match_id, account_id, semaphore):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    async with semaphore:
        try:
            async with session.get(url) as resp:
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


async def fetch_last_matches_detailed_pro_async(account_id, limit=100):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        # 1. Получаем список всех про матчей
        pro_matches_url = "https://api.opendota.com/api/proMatches"
        async with session.get(pro_matches_url) as resp:
            if resp.status != 200:
                print(f"[ERROR] Failed to fetch pro matches, status: {resp.status}")
                return []

            pro_matches = await resp.json()
            print(f"[INFO] Fetched {len(pro_matches)} pro matches")

        # 2. Отбираем первые N матчей
        match_ids = [m["match_id"] for m in pro_matches][:limit]
        print(f"[INFO] Checking {len(match_ids)} matches for player {account_id}")

        tasks = [fetch_match_details(session, match_id, account_id, semaphore) for match_id in match_ids]
        results = await asyncio.gather(*tasks)

        valid_results = [r for r in results if r]
        print(f"[INFO] Found {len(valid_results)} matches with player {account_id}")
        return valid_results


def fetch_last_matches_simple(account_id: int, limit: int = 100):
    url = f"https://api.opendota.com/api/players/{account_id}/matches"
    params = {
        "limit": limit,
        "lobby_type": 1,
    }
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch simple matches: {e}")
        return []



async def fetch_player_profile_async(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

def fetch_player_profile(account_id):
    return asyncio.run(fetch_player_profile_async(account_id))

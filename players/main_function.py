import requests
import asyncio
import aiohttp

ALLOWED_GAME_MODES = {1, 2, 3, 4, 5, 22}

ALLOWED_LOBBY_TYPES = {0, 2, 5, 6, 7, 9}

MAX_CONCURRENT_REQUESTS = 5  # Ограничим одновременные запросы

# Общий семафор
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

async def fetch_match(session, match_id, account_id, semaphore, retries=3):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    async with semaphore:
        for attempt in range(retries):
            try:
                async with session.get(url) as resp:
                    if resp.status == 429:
                        wait = 3 + attempt * 2
                        await asyncio.sleep(wait)
                        continue
                    elif resp.status != 200:
                        return None

                    full_match = await resp.json()
                    game_mode = full_match.get("game_mode")
                    lobby_type = full_match.get("lobby_type")

                    if game_mode not in ALLOWED_GAME_MODES or lobby_type not in ALLOWED_LOBBY_TYPES:
                        return None

                    player_data = next(
                        (p for p in full_match.get("players", []) if p.get("account_id") == account_id), None)
                    if not player_data:
                        return None

                    player_data["match_id"] = match_id
                    return player_data

            except Exception as e:
                await asyncio.sleep(1)
        return None


async def fetch_last_matches_detailed_async(account_id, limit=100, progress_callback=None):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession() as session:
        base_url = f"https://api.opendota.com/api/players/{account_id}/matches?limit={limit}"
        async with session.get(base_url) as resp:
            if resp.status != 200:
                return []

            basic_matches = await resp.json()

        batch_size = 15
        detailed_matches = []

        for i in range(0, len(basic_matches), batch_size):
            batch = basic_matches[i:i + batch_size]
            tasks = [fetch_match(session, m['match_id'], account_id, semaphore) for m in batch if m.get('match_id')]
            results = await asyncio.gather(*tasks)
            valid_results = [r for r in results if r]
            detailed_matches.extend(valid_results)

            if progress_callback:
                progress_callback(len(detailed_matches), limit)

            await asyncio.sleep(0.7)

        return detailed_matches

def fetch_last_matches_detailed(account_id, limit=100, progress_callback=None):
    return asyncio.run(fetch_last_matches_detailed_async(account_id, limit, progress_callback))


def fetch_player_profile(account_id):
    url = f"https://api.opendota.com/api/players/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        profile = response.json()
        mmr_estimate = profile.get("mmr_estimate", {}).get("estimate", 0)
        profile["real_mmr_score"] = mmr_estimate
        return profile
    return {}


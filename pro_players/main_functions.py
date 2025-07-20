import json
import aiohttp
import requests
from collections import Counter
from pro_players.main_function import fetch_player_profile, fetch_last_pro_matches_for_player
from players.main_functions import (
    calculate_skill_score,
    get_roles_from_matches,
    calculate_transfer_price,
    load_rank_mapping,
    calculate_salary
)
from players.classification import (
    normalize_roles_for_modifier,
    calculate_role_modifier,
    classify_player
)
from heroes.main_functions import is_win

# Загрузка словаря героев
with open('data/heroes.json', encoding='utf-8') as f:
    heroes_dict = json.load(f)

def is_pro_player(account_id):
    response = requests.get("https://api.opendota.com/api/proPlayers")
    if response.status_code == 200:
        players = response.json()
        return any(p["account_id"] == account_id for p in players)
    return False

def get_hero_name(hero_id):
    return heroes_dict.get(str(hero_id), f"Unknown Hero ({hero_id})")

def calculate_hero_winrate(matches):
    hero_counts = Counter()
    hero_wins = Counter()

    for match in matches:
        hero_id = match.get('hero_id')
        if hero_id is None:
            continue
        hero_counts[hero_id] += 1
        if is_win(match):
            hero_wins[hero_id] += 1

    return hero_counts, hero_wins

def get_top_heroes_with_winrate(matches, top_n=5):
    hero_counts, hero_wins = calculate_hero_winrate(matches)
    top_heroes = hero_counts.most_common(top_n)
    result = []
    for hero_id, count in top_heroes:
        wins = hero_wins.get(hero_id, 0)
        winrate = (wins / count) * 100 if count > 0 else 0
        hero_name = get_hero_name(hero_id)
        result.append({
            'hero_name': hero_name,
            'count': count,
            'winrate': winrate
        })
    return result

async def get_pro_player_team(account_id):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.opendota.com/api/proPlayers") as response:
            if response.status == 200:
                players = await response.json()
                for p in players:
                    if p["account_id"] == account_id:
                        return p.get("team_name", "Неизвестно\Нет")
            return "Неизвестно"

async def analyze_pro_player(account_id: int, match_limit: int = 100):
    profile = await fetch_player_profile(account_id)

    if not profile:
        return None, "Ошибка загрузки профиля игрока"

    matches = await fetch_last_pro_matches_for_player(account_id, match_limit)

    if not matches:
        return None, "Недостаточно матчей для анализа"
    elif len(matches) < 10:
        return None, "Недостаточно матчей для анализа"

    rank_mapping = load_rank_mapping()
    rank_tier = profile.get("rank_tier", 0)
    rank_info = rank_mapping.get(str(rank_tier), {"name": "неизвестно", "mmr": 0})
    rank_name = rank_info["name"]
    estimated_mmr = rank_info["mmr"]
    real_mmr = profile.get("real_mmr_score", 0)

    if real_mmr >= 3000:
        mmr_text = str(real_mmr)
        mmr_for_calc = real_mmr
    elif real_mmr > 0:
        mmr_text = "ниже 3000"
        mmr_for_calc = 0
    elif estimated_mmr > 0:
        mmr_text = f"~{rank_info['mmr']} (по рангу: {rank_name})"
        mmr_for_calc = estimated_mmr
    else:
        mmr_text = "не определён"
        mmr_for_calc = 0

    skill_score = calculate_skill_score(matches)
    skill_score = max(skill_score, 0)

    roles = get_roles_from_matches(matches)
    normalized_roles = normalize_roles_for_modifier(roles)
    role_modifier, versatility_bonus = calculate_role_modifier(normalized_roles)
    player_class = classify_player(matches)

    transfer_price = calculate_transfer_price(
        skill_score=skill_score,
        mmr=mmr_for_calc,
        media_score=3,
        role_modifier=role_modifier,
        behavior_coeff=1.0,
        versatility_bonus=versatility_bonus
    )

    salary = calculate_salary(
        transfer_price=transfer_price,
        mmr=mmr_for_calc,
        role_modifier=role_modifier,
        behavior_coeff=1.0,
        media_score=3
    )

    top_heroes = get_top_heroes_with_winrate(matches)
    team_name = await get_pro_player_team(account_id)

    nickname = profile.get("profile", {}).get("personaname", "Unknown Player")

    result = {
        "account_id": account_id,
        "nickname": nickname,
        "skill_score": skill_score,
        "rank_name": rank_name,
        "mmr_text": mmr_text,
        "roles": roles,
        "role_modifier": role_modifier,
        "versatility_bonus": versatility_bonus,
        "player_class": player_class,
        "transfer_price": transfer_price,
        "salary": salary,
        "top_heroes": top_heroes,
        "team_name": team_name
    }

    return result, None
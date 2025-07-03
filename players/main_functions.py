from heroes.main_functions import is_win
from collections import defaultdict
import os
import json

_rank_mapping = None

def load_rank_mapping():
    global _rank_mapping
    if _rank_mapping is None:
        file_path = os.path.join("data", "ranks.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                _rank_mapping = json.load(f)
        except Exception as e:
            print(f"❌ Не удалось загрузить ranks.json: {e}")
            _rank_mapping = {}
    return _rank_mapping


def calculate_winrate(matches):
    wins = sum(1 for m in matches if is_win(m))
    return wins / len(matches)

def calculate_skill_score(matches):
    if not matches:
        return 0

    total_kills = sum(m['kills'] for m in matches)
    total_assists = sum(m['assists'] for m in matches)
    total_deaths = sum(m['deaths'] if m['deaths'] > 0 else 1 for m in matches)
    kda_ratio = (total_kills + total_assists) / total_deaths
    kda_score = min(kda_ratio / 5 * 20, 20)  # Нормализация

    avg_gpm = sum(m.get('gold_per_min', 0) for m in matches) / len(matches)
    avg_xpm = sum(m.get('xp_per_min', 0) for m in matches) / len(matches)
    gpm_xpm_score = min(((avg_gpm + avg_xpm) / 2 - 300) / 5, 10)

    winrate = calculate_winrate(matches)
    winrate_score = winrate * 10

    total_team_kills = sum(m['kills'] + m['assists'] for m in matches) + 1
    fight_participation = (total_kills + total_assists) / total_team_kills
    fight_score = min(fight_participation * 10, 10)


    hero_counts = defaultdict(int)
    for m in matches:
        hero_counts[m['hero_id']] += 1
    diverse_heroes = sum(1 for count in hero_counts.values() if count >= 3)
    hero_pool_score = max(min(diverse_heroes / 10 * 10, 10), 0)

    total = kda_score + gpm_xpm_score + winrate_score + fight_score + hero_pool_score
    return round(total, 2)

def get_roles_from_matches(matches):
    from collections import defaultdict
    role_counts = defaultdict(int)

    for m in matches:
        lane_role = m.get('lane_role')
        role = m.get('role')
        ps = m.get('player_slot')

        if lane_role is not None:
            # Обычно lane_role: 1=carry, 2=mid, 3=offlane, 4=support4, 5=support5
            if lane_role == 1:
                role_counts['carry'] += 1
            elif lane_role == 2:
                role_counts['mid'] += 1
            elif lane_role == 3:
                role_counts['offlane'] += 1
            elif lane_role == 4:
                role_counts['support4'] += 1
            elif lane_role == 5:
                role_counts['support5'] += 1
        elif role is not None:
            # Если есть role, он тоже кодирует позиции аналогично lane_role
            if role == 1:
                role_counts['carry'] += 1
            elif role == 2:
                role_counts['mid'] += 1
            elif role == 3:
                role_counts['offlane'] += 1
            elif role == 4:
                role_counts['support4'] += 1
            elif role == 5:
                role_counts['support5'] += 1
        elif ps is not None:
            # fallback по player_slot
            # Radiant slots 0-4, Dire slots 128-132
            slot = ps if ps < 128 else ps - 128
            # распределяем примерно:
            if slot == 0:
                role_counts['carry'] += 1
            elif slot == 1:
                role_counts['mid'] += 1
            elif slot == 2:
                role_counts['offlane'] += 1
            elif slot == 3:
                role_counts['support4'] += 1
            else:
                role_counts['support5'] += 1

    # Фильтр по количеству матчей на роли, например, минимум 10
    filtered_roles = {role for role, count in role_counts.items() if count >= 10}
    return filtered_roles


def calculate_transfer_price(skill_score, mmr, media_score,
                             role_modifier=1.0, behavior_coeff=1.0,
                             versatility_bonus=1.0, base_rate=1000):
    mmr_score = min(max((mmr - 4000) / 200 * 1.5, 0), 15)
    total_score = (skill_score + mmr_score + media_score)
    adjusted_score = total_score * role_modifier * behavior_coeff * versatility_bonus
    transfer_price = adjusted_score * base_rate
    return round(transfer_price, 2)


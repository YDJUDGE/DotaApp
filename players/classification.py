
def classify_player(matches):
    total_hero_damage = sum(m.get('hero_damage', 0) for m in matches)
    total_tower_damage = sum(m.get('tower_damage', 0) for m in matches)
    total_healing = sum(m.get('hero_healing', 0) for m in matches)

    avg_hero_damage = total_hero_damage / len(matches)
    avg_tower_damage = total_tower_damage / len(matches)
    avg_healing = total_healing / len(matches)

    total = avg_hero_damage + avg_tower_damage + avg_healing + 1e-6

    dmg_share = avg_hero_damage / total
    tower_share = avg_tower_damage / total
    heal_share = avg_healing / total

    is_healer = heal_share >= 0.13
    is_pusher = tower_share >= 0.20
    is_damage_dealer = dmg_share >= 0.6

    if is_healer and is_pusher:
        return "Поддержка-Пушер"
    elif is_healer and is_damage_dealer:
        return "Боевая поддержка"
    elif is_pusher and is_damage_dealer:
        return "Гибрид: Воин-Пушер"
    elif is_damage_dealer and tower_share > 0.15:
        return "Воин с уклоном в пуш"
    elif is_healer:
        return "Хорошая поддержка / Доктор"
    elif is_pusher:
        return "Разрушитель построек"
    elif is_damage_dealer:
        return "Инициатор / Воин"
    else:
        return "Универсальный игрок"


def normalize_roles_for_modifier(roles):
    """
    Преобразует роли, возвращаемые get_roles_from_matches (например, 'Carry', 'Support'),
    в формат ролей, ожидаемый calculate_role_modifier ('carry', 'mid', 'offlane', 'support4', 'support5').
    """
    mapping = {
        "Carry": "carry",
        "Support": "support5",
        "Initiator": "offlane",
        "Pusher": "mid",
        "Durable": "support4",  # танк/универсал
        "Disabler": "support4",
        "Nuker": "mid",
        "Jungler": "offlane",
        "Escape": "mid",
    }
    normalized = set()
    for role in roles:
        role_lower = mapping.get(role)
        if role_lower:
            normalized.add(role_lower)
    return normalized

def calculate_role_modifier(roles):
    # Приоритет ролей для максимального множителя
    if {'carry', 'mid', 'offlane'}.issubset(roles):
        return 1.2, 1.015
    elif {'offlane', 'support4', 'support5'}.issubset(roles):
        return 1.0, 1.013
    elif {'mid', 'offlane', 'support4'}.issubset(roles):
        return 1.1, 1.012
    elif {'carry', 'support4', 'support5'}.issubset(roles):
        return 1.1, 1.01
    else:
        # Если менее 3 ролей, даём множитель для самой частой роли
        if 'mid' in roles:
            return 1.2, 1.0
        elif 'carry' in roles:
            return 1.1, 1.0
        elif 'offlane' in roles:
            return 1.0, 1.0
        elif 'support4' in roles:
            return 0.95, 1.0
        elif 'support5' in roles:
            return 0.9, 1.0
        else:
            return 1.0, 1.0
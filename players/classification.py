
def classify_player(matches):
    total_hero_damage = sum(m.get('hero_damage', 0) for m in matches)
    total_tower_damage = sum(m.get('tower_damage', 0) for m in matches)
    total_healing = sum(m.get('hero_healing', 0) for m in matches)

    total = total_hero_damage + total_tower_damage + total_healing + 1

    hero_damage_share = total_hero_damage / total
    tower_damage_share = total_tower_damage / total
    healing_share = total_healing / total

    if hero_damage_share > tower_damage_share and hero_damage_share > healing_share:
        return "Инициатор / Воин"
    elif tower_damage_share > hero_damage_share and tower_damage_share > healing_share:
        return "Разрушитель построек"
    elif healing_share > hero_damage_share and healing_share > tower_damage_share:
        return "Хорошая поддержка / Доктор"
    else:
        return "Универсальный игрок"


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
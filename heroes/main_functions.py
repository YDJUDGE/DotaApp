
def is_win(match):
    """Победил игрок или нет"""
    slot = match['player_slot']
    is_radiant = slot < 128
    return match['radiant_win'] == is_radiant

def format_duration(seconds):
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02}"

def calculate_kda(kills, deaths, assists):
    return (kills + assists) / max(1, deaths)



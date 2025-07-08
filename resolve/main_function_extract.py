import re

def steam64_to_steam32(steam64: int) -> int:
    """Стандартное смещение VALVE"""
    BASE_ID = 76561197960265728
    if steam64 < BASE_ID:
        raise ValueError("Некорректный Steam64 ID")
    return steam64 - BASE_ID


def extract_steam64(input_str):
    """Сама функция извлечения"""
    # Просто число
    if input_str.isdigit() and len(input_str) >= 17:
        return int(input_str)

    # Ссылка с /profiles/
    match = re.search(r"profiles/(\d{17})", input_str)
    if match:
        return int(match.group(1))

    return None

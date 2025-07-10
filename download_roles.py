import os
import json

role_mapping = {
    "Carry": "Повелитель урона",
    "Support": "Поддержка",
    "Disabler": "Контролирует файты",
    "Initiator": "Инициатор",
    "Durable": "Танк",
    "Escape": "Маневренный",
    "Pusher": "Пушер",
    "Nuker": "Нюкер",
    "Jungler": "Лесник"
}

os.makedirs("data", exist_ok=True)
with open("data/role.json", "w", encoding="utf-8") as f:
    json.dump(role_mapping, f, ensure_ascii=False, indent=4)

print("✅ Файл data/role.json успешно создан")

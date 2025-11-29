import os
import random
from datetime import datetime

# Папка репозитория
repo_dir = os.path.dirname(os.path.abspath(__file__))

txt_file = os.path.join(repo_dir, "Memory.txt")
xml_file = os.path.join(repo_dir, "Memory.xml")

# Проверяем, что Memory.txt существует
if not os.path.exists(txt_file):
    print(f"Файл {txt_file} не найден! Прерываем скрипт.")
    exit(0)

# Читаем Memory.txt
with open(txt_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

if not lines:
    print("Memory.txt пустой. Выходим без изменений.")
    exit(0)

# Перемешиваем задачи
random.shuffle(lines)

# Категории
category_map = {"!":"A", "*":"B", "-":"C", "~":"D"}
today = datetime.today().date()
rss_items = []

for line in lines:
    parts = line.split("|")
    symbol_task = parts[0].strip()
    deadline_str = parts[1].strip() if len(parts) > 1 else ""

    marker = ""
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            if deadline <= today:

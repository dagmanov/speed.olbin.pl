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

# Читаем Memory.txt и всегда создаём переменную lines
lines = []
try:
    with open(txt_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
except Exception as e:
    print(f"Ошибка при чтении Memory.txt: {e}")
    exit(0)

# Если файл пустой, выходим
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
                marker = " 🔴"
        except Exception as e:
            print(f"Неверная дата '{deadline_str}' в строке '{line}': {e}")

    symbol = symbol_task[0]
    category = category_map.get(symbol, "D")
    task_title = symbol_task[1:].strip() + marker

    # Экранируем XML-символы
    task_title = task_title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    rss_items.append(f"""
<item>
<title>{task_title}</title>
<description>Категория: {category}</description>
<pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
<category>{category}</category>
</item>
""")

# Генерируем RSS
rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Memory – Мои задачи</title>
<link>local-memory</link>
<description>Живые обновления моих задач</description>
{''.join(rss_items)}
</channel>
</rss>
"""

# Сохраняем Memory.xml
try:
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(rss_feed)
    print(f"Memory.xml сгенерирован! ({len(rss_items)} задач)")
except Exception as e:
    print(f"Ошибка при записи Memory.xml: {e}")

import os
from datetime import datetime, timezone
import html

# --- Настройки ---
REPO_URL = "https://<username>.github.io/<repo>/Memory.xml"  # твой публичный GitHub Pages URL

# Папка репозитория
repo_dir = os.path.dirname(os.path.abspath(__file__))

txt_file = os.path.join(repo_dir, "Memory.txt")
xml_file = os.path.join(repo_dir, "Memory.xml")

# --- Проверяем, что Memory.txt существует ---
if not os.path.exists(txt_file):
    print(f"Файл {txt_file} не найден! Прерываем скрипт.")
    exit(0)

# --- Читаем Memory.txt ---
with open(txt_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

if not lines:
    print("Memory.txt пустой. Выходим без изменений.")
    exit(0)

# --- Категории по символам приоритета ---
category_map = {"!": "A", "*": "B", "-": "C", "~": "D"}
priority_order = {"A": 1, "B": 2, "C": 3, "D": 4}

# --- Сортируем задачи по приоритету ---
tasks = []
for line in lines:
    symbol_task = line[0]
    category = category_map.get(symbol_task, "D")
    tasks.append((priority_order[category], line, category))

# Сортируем по числовому приоритету (1=A, 2=B, 3=C, 4=D)
tasks.sort(key=lambda x: x[0])

# --- Создаём RSS items ---
rss_items = []
for idx, (_, line, category) in enumerate(tasks, start=1):
    parts = line.split("|")
    title = html.escape(line)
    description = html.escape(parts[1].strip()) if len(parts) > 1 else ""
    pubdate = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000')
    guid = f"task-{idx}"

    item_xml = f"""
    <item>
        <title>{title}</title>
        <link>{REPO_URL}</link>
        <description>{description}</description>
        <category>{category}</category>
        <guid>{guid}</guid>
        <pubDate>{pubdate}</pubDate>
    </item>
    """
    rss_items.append(item_xml)

# --- Формируем RSS-файл ---
rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>Memory – Мои задачи</title>
    <link>{REPO_URL}</link>
    <description>Живые обновления моих задач</description>
    <atom:link href="{REPO_URL}" rel="self" type="application/rss+xml" />
    {''.join(rss_items)}
</channel>
</rss>
"""

# --- Сохраняем в Memory.xml ---
with open(xml_file, "w", encoding="utf-8") as f:
    f.write(rss_feed.strip())

print(f"Memory.xml сгенерирован! ({len(tasks)} задач)")
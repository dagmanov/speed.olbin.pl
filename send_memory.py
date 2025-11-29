import os
import random
from datetime import datetime

repo_dir = os.path.dirname(os.path.abspath(__file__))
txt_file = os.path.join(repo_dir, "memory.txt")
xml_file = os.path.join(repo_dir, "memory.xml")

# Читаем задачи
with open(txt_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Перемешиваем задачи
random.shuffle(lines)

# Генерируем RSS
category_map = {"!":"A", "*":"B", "-":"C", "~":"D"}
rss_items = []
today = datetime.today().date()

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
        except:
            pass

    symbol = symbol_task[0]
    category = category_map.get(symbol, "D")
    task_title = symbol_task[1:].strip() + marker

    rss_items.append(f"""
<item>
<title>{task_title}</title>
<description>Категория: {category}</description>
<pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
<category>{category}</category>
</item>
""")

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

# Сохраняем memory.xml
with open(xml_file, "w", encoding="utf-8") as f:
    f.write(rss_feed)

print("memory.xml сгенерирован!")

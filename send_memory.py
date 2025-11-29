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

    rss_items.append(f"""
<item>
<title>{task_title}</title>
<description>Категория: {category}</description>
<pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
<category>{category}</category>
</item>
""")

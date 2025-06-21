import emoji, re, os

def option(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    emoticon_path = os.path.join(current_dir, "emoticon_dict.txt")
    
    emot = {}
    with open(emoticon_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                emot[parts[0]] = parts[1]

    pattern = re.compile('|'.join(map(re.escape, emot)))

    return data.astype(str).applymap(
        lambda x: pattern.sub(lambda m: emot[m.group()], emoji.replace_emoji(x, replace=''))
    )

import emoji, re

def option(data):
    with open('emoticon_dict.txt', 'r') as f:
        emot = dict(line.strip().split(None, 1) for line in f)

    pattern = re.compile('|'.join(map(re.escape, emot)))

    return data.astype(str).applymap(
        lambda x: pattern.sub(lambda m: emot[m.group()], emoji.replace_emoji(x, replace=''))
    )

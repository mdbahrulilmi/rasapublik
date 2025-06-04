import emoji

def option(data):
    return data.astype(str).applymap(lambda x: emoji.replace_emoji(x, replace=''))
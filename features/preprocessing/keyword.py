def option(data, words, text_column='tweet'):
    pattern = '|'.join(words)
    data = data[data[text_column].str.contains(pattern, case=False, na=False)]
    return data

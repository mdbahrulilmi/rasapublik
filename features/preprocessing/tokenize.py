from nltk.tokenize import word_tokenize

def option(data, text_column='tweet'):
    data[text_column] = data[text_column].apply(lambda x: word_tokenize(str(x)))
    return data

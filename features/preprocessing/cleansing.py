import re
def option(data):
    cleansing = data.astype(str).applymap(lambda x: re.sub(r'[^a-zA-Z ]', ' ',x))
    return cleansing
import re
import pandas as pd

def convert_negation(text):
    # Peta kata tidak baku ke baku
    replacements = {
        "ga": "tidak",
        "gak": "tidak",
        "nggak": "tidak",
        "tak": "tidak",
        "bukan": "bukan",
        "tidak": "tidak",
        "di": "di",
        "haus" : "haus",
        'dianggap' : 'dianggap'
    }

    negation_pattern = r'\b(' + '|'.join(replacements.keys()) + r')\s+(\w+)\b'

    def replacer(match):
        neg = match.group(1)
        word = match.group(2)
        standard_neg = replacements.get(neg, neg)
        return f"{standard_neg}_{word}"

    return re.sub(negation_pattern, replacer, str(text))  # pastikan input string

def option(data):
    if isinstance(data, str):
        return convert_negation(data)
    elif isinstance(data, pd.Series):
        return data.astype(str).apply(convert_negation)
    elif isinstance(data, pd.DataFrame):
        return data.astype(str).applymap(convert_negation)
    else:
        raise TypeError("Input harus berupa str, pandas.Series, atau pandas.DataFrame")

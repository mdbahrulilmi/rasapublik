import re

def option(data):
    return data.astype(str).applymap(convert_negation)

def convert_negation(text):
    negation_pattern = r'\b(tidak|bukan|ga|nggak|gak|tak|di)\s+(\w+)\b'
    
    return re.sub(negation_pattern, r'\1_\2', text)
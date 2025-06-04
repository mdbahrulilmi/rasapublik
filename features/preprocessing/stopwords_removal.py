import streamlit as st
import re
import os
from nltk.corpus import stopwords

def option(data, text_column):
    data[text_column] = data[text_column].apply(remove_stopwords_from_text)
    return data

def remove_stopwords_from_text(text):
    nltk_stopwords = set(stopwords.words('indonesian'))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    stopwords_path = os.path.join(current_dir, "stopwords-indonesia.txt")
    
    with open(stopwords_path, "r", encoding="utf-8") as f:
        custom_stopwords = set(word.strip().lower() for word in f.readlines())

    all_stopwords = nltk_stopwords.union(custom_stopwords)

    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in all_stopwords]

    return ' '.join(filtered_words)


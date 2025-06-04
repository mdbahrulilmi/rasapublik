import streamlit as st
from features.preprocessing import missing_values, casefolding, cleansing, stopwords_removal, convert_emoticon, convert_negation, tokenize

def option():
    if 'filtered_data' in st.session_state:
        data = st.session_state['filtered_data']
    else:
        data = st.session_state['selected_only_data']

    missingvalues_checkbox = st.sidebar.checkbox("Hapus nilai hilang")
    casefolding_checkbox = st.sidebar.checkbox("Ubah ke huruf kecil")
    cleansing_checkbox = st.sidebar.checkbox("Hapus karakter khusus")
    stopwordremoval_checkbox = st.sidebar.checkbox("Hapus kata stopword")
    convertEmoticon_checkbox = st.sidebar.checkbox("Hapus emotikon")
    convertNegation_checkbox = st.sidebar.checkbox("Atur negasi")
    tokenisasi_checkbox = st.sidebar.checkbox("Tokenisasi teks")


    if (
        not missingvalues_checkbox and not
        casefolding_checkbox and not
        cleansing_checkbox and not
        stopwordremoval_checkbox and not
        convertEmoticon_checkbox and not
        convertNegation_checkbox and not
        tokenisasi_checkbox
        ):
        if "filtered_data" in st.session_state:
            del st.session_state["filtered_data"]
        return st.session_state["selected_only_data"]
        
    if stopwordremoval_checkbox or tokenisasi_checkbox:
        selected_column = st.sidebar.selectbox("Pilih Kolom", st.session_state['selected_only_data'].columns)
    else:
        selected_column = None
    if missingvalues_checkbox:
        data, _ = missing_values.option(data)

    if casefolding_checkbox:
        data = casefolding.option(data)

    if cleansing_checkbox:
        data = cleansing.option(data)

    if convertEmoticon_checkbox:
        data = convert_emoticon.option(data)

    if convertNegation_checkbox:
        data = convert_negation.option(data)

    if selected_column:
        if stopwordremoval_checkbox:
            data = stopwords_removal.option(data, selected_column)
        if tokenisasi_checkbox:
            data = tokenize.option(data, selected_column)
        
    return data
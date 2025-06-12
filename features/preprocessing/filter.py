import streamlit as st
from features.preprocessing import missing_values, casefolding, cleansing, stopwords_removal, convert_emoticon, convert_negation, tokenize

def option():
    if 'filtered_data' in st.session_state:
        data = st.session_state['filtered_data']
    else:
        data = st.session_state['selected_only_data']
    
    filtering_basic = st.sidebar.expander(" Bersih Data Ringan",expanded=True)
    filtering_advanced = st.sidebar.expander("Bersih Data Lanjutan")    

    with filtering_basic:
        filtering_advanced.expanded == True
        missingvalues_checkbox = st.checkbox("Hapus nilai hilang")
        casefolding_checkbox = st.checkbox("Ubah ke huruf kecil")
        cleansing_checkbox = st.checkbox("Hapus karakter khusus")

    with filtering_advanced:
        filtering_basic.expanded == False
        stopwordremoval_checkbox = st.checkbox("Hapus kata stopword")
        convertEmoticon_checkbox = st.checkbox("Hapus emotikon")
        convertNegation_checkbox = st.checkbox("Atur negasi")
        tokenisasi_checkbox = st.checkbox("Tokenisasi teks")


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
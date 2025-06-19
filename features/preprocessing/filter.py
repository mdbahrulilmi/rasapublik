import streamlit as st
from features.preprocessing import keyword, missing_values, casefolding, cleansing, stopwords_removal, convert_emoticon, convert_negation, tokenize, undersampling

def option():
    if 'filtered_data' in st.session_state:
        data = st.session_state['filtered_data']
    else:
        data = st.session_state['selected_only_data']
    
    filtering_basic = st.sidebar.expander(" Bersih Data Ringan",expanded=True)
    filtering_advanced = st.sidebar.expander("Bersih Data Lanjutan")
    filtering_sampling = st.sidebar.expander("Sampling")    

    with filtering_basic:
        filtering_advanced.expanded == False
        filtering_sampling.expanded == False
        missingvalues_checkbox = st.checkbox("Hapus nilai hilang")
        casefolding_checkbox = st.checkbox("Ubah ke huruf kecil")
        cleansing_checkbox = st.checkbox("Hapus karakter khusus")
        keywordFiltering_checkbox = st.checkbox("Pencocokan teks")

    with filtering_advanced:
        filtering_basic.expanded == False
        filtering_sampling.expanded == False
        stopwordremoval_checkbox = st.checkbox("Hapus kata stopword")
        convertEmoticon_checkbox = st.checkbox("Hapus emotikon")
        convertNegation_checkbox = st.checkbox("Atur negasi")
        tokenisasi_checkbox = st.checkbox("Tokenisasi teks")
    
    with filtering_sampling:
        undersampling_checkbox = st.checkbox("Undersampling")
    if (
        not missingvalues_checkbox and not
        casefolding_checkbox and not
        cleansing_checkbox and not
        stopwordremoval_checkbox and not
        convertEmoticon_checkbox and not
        convertNegation_checkbox and not
        tokenisasi_checkbox and not
        undersampling_checkbox
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

    if keywordFiltering_checkbox:
        data = keyword.option(data,['polisi','polri'],'tweet')

    if convertEmoticon_checkbox:
        data = convert_emoticon.option(data)

    if convertNegation_checkbox:
        data = convert_negation.option(data)

    if undersampling_checkbox:
        data = undersampling.option(data)
        
    if selected_column:
        if stopwordremoval_checkbox:
            data = stopwords_removal.option(data, selected_column)
        if tokenisasi_checkbox:
            data = tokenize.option(data, selected_column)

    return data
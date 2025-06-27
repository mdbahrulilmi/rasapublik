import streamlit as st
from features.labeling import rulebased

def option(data,selected_column):
    st.sidebar.subheader('Label Otomatis')
    method = st.sidebar.selectbox(
        'Pilih label otomatis',
        ("Rule Based Labeling"),
        label_visibility="collapsed"
        )
    submit = st.sidebar.button("Gunakan Metode",type="primary")

    if submit:
        if method == "Rule Based Labeling":
            labeled_data = rulebased.method(data, selected_column)
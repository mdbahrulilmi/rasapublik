import streamlit as st
import pandas as pd
from features.data import collection_data, download_data
from features.labeling import manual_labeled, sidebar
    
def update_amount():
    try:
        st.session_state['amount'] = int(st.session_state['amount_input'])
    except ValueError:
        st.session_state['amount'] = 0

@st.dialog("dataset", width="large")
def realTimeData(data,column):
    if "data_labeled" in st.session_state:
        st.dataframe(st.session_state.data_labeled)
    else:
        st.dataframe(data[column])


def main():
    col_header1, col_header2 = st.columns([0.9, 0.19], vertical_alignment="bottom")
    with col_header1:
        st.markdown("### Pilih dataset")
    with col_header2:
        dataset_preview =  st.button("Lihat dataset")
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        result = collection_data.method()
    
    if result:
        data, name = result
        with col_input2:
            selected_column = st.selectbox("Pilih Kolom", data.columns, index=1)
        with col_input3:
            if "amount" not in st.session_state:
                st.session_state.amount = 0
            st.text_input(
                label="Label manual:",
                value= str(st.session_state.amount),
                key="amount_input",
                on_change=update_amount
                )
            
        if data is not None:
            if dataset_preview:
                realTimeData(data,selected_column)
                
        if 'amount' in st.session_state:
                manual_labeled.option(data, selected_column)
    if result is not None:
        data, name = result
        if "data_labeled" in st.session_state:
            download_data.method(st.session_state.data_labeled)
            sidebar.option(st.session_state.data_labeled)
        else:
            sidebar.option(data[selected_column])
    else:
        st.warning("Belum ada dataset yang disimpan.")

main()
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
def realTimeData(data, column):
    if "data_labeled" in st.session_state:
        st.dataframe(st.session_state.data_labeled)
    else:
        st.dataframe(data[column])

def main():
    col_header1, col_header2 = st.columns([0.9, 0.19], vertical_alignment="bottom")
    with col_header1:
        st.markdown("### Pilih dataset")
    with col_header2:
        dataset_preview = st.button("Lihat dataset")

    col_input1, col_input2, col_input3 = st.columns([0.4, 0.2, 0.4])
    with col_input1:
        result = collection_data.method()

    if result:
        data, name = result

        prev_key = 'prev_dataset_column'
        current_key = f"{name}_{str(data.columns.tolist())}"
        if st.session_state.get(prev_key) != current_key:
            st.session_state.pop('data_labeled', None)
            st.session_state[prev_key] = current_key

        with col_input2:
            selected_column = st.selectbox("Pilih Kolom", data.columns, index=1)

        with col_input3:
            col_amount1, col_amount2, col_amount3 = st.columns(3, vertical_alignment="bottom")
            with col_amount1:
                start_index = st.number_input(
                    "Index awal",
                    min_value=0,
                    max_value=len(data) - 1,
                    value=st.session_state.get('start_index', 0)
                )
            with col_amount2:
                amount = st.number_input(
                    "Jumlah data",
                    min_value=1,
                    max_value=len(data) - start_index,
                    value=st.session_state.get('amount', 10)
                )
            with col_amount3:
                if st.button("Set"):
                    st.session_state['start_index'] = start_index
                    st.session_state['amount'] = amount
                    st.rerun()

        if data is not None and dataset_preview:
            realTimeData(data, selected_column)

        if 'amount' in st.session_state:
            manual_labeled.option(data, selected_column)

        if "data_labeled" in st.session_state:
            download_data.method(st.session_state.data_labeled)
            sidebar.option(st.session_state.data_labeled, selected_column)
        else:
            sidebar.option(data, selected_column)

    else:
        st.warning("Belum ada dataset yang disimpan.")

main()

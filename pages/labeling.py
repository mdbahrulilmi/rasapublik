import streamlit as st
import pandas as pd

def collection_data():
    if "data_collection" in st.session_state and st.session_state.data_collection:
        dataset_names = [item["name"] for item in st.session_state.data_collection]
        selected_name = st.selectbox("Pilih Dataset:", dataset_names)
        selected_data = next(
            (item["data"] for item in st.session_state.data_collection if item["name"] == selected_name)
        )
        return selected_data, selected_name

def main():
    st.markdown("### Pilih dataset")
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        result = collection_data()
    
    if result:
        data, name = result
        with col_input2:
            selected_column = st.selectbox("Pilih Kolom", data.columns)
        with col_input3:
            amount_input = st.text_input(label="Masukkan angka:", key=int)
            amount = int(amount_input)

    if amount:
        for i in range(amount):
            col1, col2 = st.columns([0.7, 0.3], gap="medium")
            with col1:
                st.write(data[selected_column][i+1])
            with col2:
                st.text_input(label="", placeholder=f"Label ke-{i+1}", key=f"label_{i}")

            

    else:
        st.warning("Belum ada dataset yang disimpan.")


main()
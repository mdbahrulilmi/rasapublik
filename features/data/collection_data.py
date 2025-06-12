import streamlit as st

def method():
    if "data_collection" in st.session_state and st.session_state.data_collection:
        dataset_names = [item["name"] for item in st.session_state.data_collection]
        selected_name = st.selectbox("Pilih Dataset:", dataset_names)
        selected_data = next(
            (item["data"] for item in st.session_state.data_collection if item["name"] == selected_name)
        )
        return selected_data, selected_name
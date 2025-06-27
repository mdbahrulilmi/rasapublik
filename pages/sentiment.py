import streamlit as st
from features.data import collection_data
from features.analysis import sidebar


def main():
    st.markdown("### Pilih dataset")
    selected_data = None
    selected_name = None

    result = collection_data.method()
    if result:
        selected_data, selected_name = result
        sidebar.option(selected_data, selected_name, "text", "label")
        
    else:
        st.warning("Belum ada dataset yang disimpan.")

main()

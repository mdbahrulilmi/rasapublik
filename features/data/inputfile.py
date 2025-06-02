import streamlit as st
import pandas as pd
from io import StringIO

@st.dialog("Kasih datamu nama!")
def nameData(data):
    if "data_collection" not in st.session_state:
        st.session_state.data_collection = []
    name = st.text_input("Nama Dataset")
    if st.button("Submit"):
        st.session_state.data_collection.append({
            "name": name,
            "data": data
        })
        st.rerun()

def method():
    st.write("# Silahkan Input Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Data preview: \t")
            st.write(df.head())
            if st.button("Gunakan Data"):
                nameData(df)
            
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")

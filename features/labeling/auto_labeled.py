import streamlit as st

def option():
    if 'data_labeled' in st.session_state:
            st.sidebar.checkbox('Rule Based Labeling')
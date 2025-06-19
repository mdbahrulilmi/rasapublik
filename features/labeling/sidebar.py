import streamlit as st
from features.labeling import rulebased

def option(data):
    ruleBased_checkbox = st.sidebar.checkbox('Rule Based')
    petrainedModel_checkbox = st.sidebar.checkbox('Petrained Model')
    weakSupervision_checkbox = st.sidebar.checkbox('Weak Supervision')
    if "rulebased" not in st.session_state: 
        if ruleBased_checkbox is True:
            rulebased.method(data)
    if ruleBased_checkbox is False:
        if "rulebased" in st.session_state:
            del st.session_state.rulebased

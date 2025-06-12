import streamlit as st
import pandas as pd
from features.data import collection_data
from features.labeling import manual_labeled, auto_labeled
    
def update_amount():
    try:
        st.session_state['amount'] = int(st.session_state['amount_input'])
    except ValueError:
        st.session_state['amount'] = 0

def main():
    st.markdown("### Pilih dataset")
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        result = collection_data.method()
    
    if result:
        data, name = result
        with col_input2:
            selected_column = st.selectbox("Pilih Kolom", data.columns)
        with col_input3:
            if "amount" not in st.session_state:
                st.session_state.amount = 0
            st.text_input(
                label="Masukkan angka:",
                value= str(st.session_state.amount),
                key="amount_input",
                on_change=update_amount
                )
            
    if 'amount' in st.session_state:
        if st.session_state['amount'] > 0 :
            # Manual
            manual_labeled.option(data, selected_column)
        else:
            # Auto 
            if st.button('Langsung Otomatis',type='primary'):
                st.session_state['data_labeled'] = data[selected_column]
            auto_labeled.option()
            

    else:
        st.warning("Belum ada dataset yang disimpan.")


main()
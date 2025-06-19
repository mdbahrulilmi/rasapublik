import streamlit as st

@st.dialog("Kasih datamu nama!")
def nameData(csv):
    name = st.text_input("Nama Dataset")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f'{name}.csv',
        mime="text/csv",
        icon=":material/download:",
    )

def method(data):
    csv = data.to_csv().encode('utf-8')
    if st.button('Download'):
        nameData(csv)

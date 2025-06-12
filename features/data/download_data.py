import streamlit as st

@st.dialog("Kasih datamu nama!")
def nameData(csv):
    if "filtered_data" in st.session_state:
        st.write(st.session_state['filtered_data'].shape)
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
    if st.button('Downlaod'):
        nameData(csv)

import streamlit as st
from features.data import collection_data, download_data
from features.analysis import svm, xlnet



def main():
    st.markdown("### Pilih dataset")
    selected_data = None
    selected_name = None

    result = collection_data.method()
    if result:
        selected_data, selected_name = result
        st.write(f"Dataset: {selected_name}")
        st.dataframe(selected_data.head())

        if st.sidebar.button("Jalankan SVM"):
            svm.algoritm(selected_data)

        if st.sidebar.button("Jalankan XLNet"):
            xlnet.algoritm(selected_data)

main()

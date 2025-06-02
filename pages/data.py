import streamlit as st
from features.data import inputfile, scrapping, crawling
def main():
    st.markdown("# Input Data 📁")
    st.write(""" 
        Silakan pilih metode pengambilan data melalui menu di sebelah kiri:  

        - **Input File**: Unggah file data secara manual dari komputer Anda.  
        - **Scrapping**: Ambil data langsung dari website menggunakan teknik web scraping.  
        - **Crawling**: Kumpulkan data secara otomatis dengan metode crawling pada situs target.  

        Pilih salah satu metode untuk memulai proses pengambilan data.
    """)
    st.sidebar.success("Pilih metode ambil data")


collection_method = {
    '-': main,
    'Input File': inputfile.method,
    'Scrapping': scrapping.method,
    'Crawling': crawling.method
}

methods = st.sidebar.selectbox("Choose a method", collection_method.keys())

collection_method[methods]()

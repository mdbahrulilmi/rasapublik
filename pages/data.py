import streamlit as st
from features.data import inputfile, scrapping, crawling

def main():
    if st.session_state.get("data_collection") is not None and len(st.session_state.data_collection) > 0:
            header_col1, header_col2 = st.columns([0.8, 0.2])
            with header_col1:
                st.markdown("**Nama Dataset**")
            with header_col2:
                st.markdown("**Action**")

            for idx, item in enumerate(st.session_state.data_collection):
                row_col1, row_col2 = st.columns([0.8, 0.2])
                with row_col1:
                    st.write(item["name"])
                with row_col2:
                    if st.button("Delete", key=f"delete_{idx}", use_container_width=True, type="primary"):
                        del st.session_state.data_collection[idx]

    else:
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

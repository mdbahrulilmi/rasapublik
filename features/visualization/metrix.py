import streamlit as st

def tab(df):
    st.subheader("📋 Tabel Evaluasi Lengkap")
    st.info("Tabel metrik seperti precision, recall, dan f1-score untuk setiap label.")
    st.dataframe(
        df.reset_index().rename(columns={"index": "Label"}).style.format(precision=3),
        use_container_width=True
    )
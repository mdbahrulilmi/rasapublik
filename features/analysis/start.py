import streamlit as st

def option(data, name):
    st.markdown("### 🧠 Pilih Metode Analisis")
    st.write("Silakan pilih metode yang ingin Anda gunakan untuk memproses atau menganalisis data Anda. Setiap metode memiliki pendekatan dan hasil yang berbeda.")

    st.markdown(f"#### 📄 Preview Dataset: **{name}**")
    st.dataframe(data.head())

    st.info("Gunakan sidebar di sebelah kiri untuk memilih metode yang tersedia.")

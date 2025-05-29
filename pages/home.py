import streamlit as st

def home():
    st.markdown("# RasaPublik 📢📊 \nBy Muhammad Bahrul Ilmi")

    st.markdown(
        """
        **RasaPublik** adalah aplikasi analisis sentimen berbasis web untuk memahami opini masyarakat terhadap topik tertentu, seperti institusi, produk, layanan, atau isu sosial.

        🔍 Anda dapat:
        - Menginput data dari file, teks langsung, atau hasil scraping
        - Melakukan pra-pemrosesan otomatis
        - Melihat hasil analisis sentimen
        - Menikmati visualisasi interaktif

        ### Tentang Aplikasi
        - Dibuat dengan Python dan Streamlit
        - Fokus pada opini publik dalam bahasa Indonesia
        - Mendukung input fleksibel dan visualisasi menarik

        ### Tujuan
        Memberikan wawasan terhadap bagaimana masyarakat memandang suatu topik atau entitas melalui data digital.
        """
    )

home()

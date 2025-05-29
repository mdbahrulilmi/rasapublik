import streamlit as st

st.logo("assets/logo.png")

pages = [
    st.Page("pages/home.py", title="Home Page", icon="🏠"),
    st.Page("pages/data.py", title="Input Data", icon="📰"),
    st.Page("pages/preprocessing.py", title="Pra Proses", icon="📝"),
    st.Page("pages/sentiment.py", title="Analisis Sentimen", icon="👨‍🏫"),
    st.Page("pages/visualization.py", title="Visualisasi", icon="📺")
]

pg = st.navigation(pages)

pg.run()
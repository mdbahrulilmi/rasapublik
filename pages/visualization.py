import streamlit as st
import pandas as pd

from features.visualization import distribution, label_model, prediction, metrix, confusion 

st.markdown("## 📊 Visualisasi Hasil Analisis Sentimen")

if 'visualisasi' not in st.session_state:
    st.warning("⚠️ Belum ada data visualisasi. Silakan lakukan analisis terlebih dahulu.")
else:
    data = st.session_state.visualisasi
    report_df = data["classification_report"]
    cm_df = data["confusion_matrix"]
    result_df = data["hasil_prediksi"]
    model = st.session_state.get("trained_model", None)
    vectorizer = st.session_state.get("vectorizer", None)
    label_encoder = st.session_state.get("label_encoder", None)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Evaluasi", 
        "📊 Grafik Label", 
        "🧱 Confusion Matrix", 
        "🥧 Distribusi", 
        "🔍 Uji Coba Prediksi"
    ])

    with tab1:
        metrix.tab(report_df)

    with tab2:
        label_model.tab(report_df)

    with tab3:
        confusion.tab(cm_df)

    with tab4:
       distribution.tab(result_df)

    with tab5:
        prediction.tab()


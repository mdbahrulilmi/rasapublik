import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

st.markdown("# Visualization page 📺")
st.sidebar.markdown("# Visualization page 📺")

if 'visualisasi' not in st.session_state:
    st.warning("⚠️ Belum ada data visualisasi. Silakan lakukan analisis terlebih dahulu.")
else:
    data = st.session_state.visualisasi
    report_df = data["classification_report"]
    cm_df = data["confusion_matrix"]
    result_df = data["hasil_prediksi"]

    # 1. Classification Report
    st.markdown("### 📊 Classification Report")
    st.dataframe(report_df.style.format(precision=3))

    # 2. Confusion Matrix
    st.markdown("### 🧱 Confusion Matrix")
    fig, ax = plt.subplots()
    sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    st.pyplot(fig)

    # 3. Tabel Hasil Prediksi
    st.markdown("### 📄 Hasil Prediksi")
    st.dataframe(result_df.head())

    # 4. Download CSV
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(result_df)

    st.download_button(
        label="📥 Download Hasil sebagai CSV",
        data=csv,
        file_name='hasil_klasifikasi_svm.csv',
        mime='text/csv',
    )

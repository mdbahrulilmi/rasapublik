import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.markdown("## 📊 Visualisasi Hasil Analisis Sentimen")

if 'visualisasi' not in st.session_state:
    st.warning("⚠️ Belum ada data visualisasi. Silakan lakukan analisis terlebih dahulu.")
else:
    data = st.session_state.visualisasi
    report_df = data["classification_report"]
    cm_df = data["confusion_matrix"]
    result_df = data["hasil_prediksi"]

    # 🔹 1. Tabel Evaluasi Lengkap
    st.markdown("### 📋 Tabel Evaluasi Lengkap")
    st.dataframe(
        report_df.reset_index().rename(columns={"index": "Label"}).style.format(precision=3),
        use_container_width=True
    )

    # 🔹 2. Grafik Bar: precision, recall, f1-score per label
    metric_df = report_df.iloc[:-3][["precision", "recall", "f1-score"]].reset_index().rename(columns={'index': 'Label'})
    metric_melted = metric_df.melt(id_vars='Label', var_name='Metrik', value_name='Skor')

    fig_metrics = px.bar(
        metric_melted,
        x='Label',
        y='Skor',
        color='Metrik',
        barmode='group',
        text_auto='.2f',
        color_discrete_sequence=px.colors.qualitative.Set2,
        title='Evaluasi Performa Model per Label'
    )
    st.plotly_chart(fig_metrics, use_container_width=True)

    # 🔹 3. Confusion Matrix
    st.markdown("### 🧱 Confusion Matrix")
    fig_cm = go.Figure(data=go.Heatmap(
        z=cm_df.values,
        x=cm_df.columns,
        y=cm_df.index,
        colorscale='Blues',
        showscale=True,
        hovertemplate="Prediksi: %{x}<br>Aktual: %{y}<br>Jumlah: %{z}<extra></extra>"
    ))
    fig_cm.update_layout(
        xaxis_title="Predicted",
        yaxis_title="Actual",
        title="Confusion Matrix",
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_cm, use_container_width=True)

    # 🔹 4. Pie Chart Distribusi Prediksi
    st.markdown("### 🥧 Distribusi Label yang Diprediksi")
    pred_counts = result_df["predicted_label"].value_counts().reset_index()
    pred_counts.columns = ["Label", "Jumlah"]

    fig_pie = px.pie(
        pred_counts,
        values="Jumlah",
        names="Label",
        title="Distribusi Prediksi",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    # 🔹 5. Filter Prediksi Salah
    st.markdown("### ❌ Prediksi yang Salah")
    result_df["status"] = result_df["actual_label"] == result_df["predicted_label"]
    salah_prediksi = result_df[~result_df["status"]]

    st.write(f"Jumlah salah prediksi: {len(salah_prediksi)}")
    st.dataframe(salah_prediksi.drop(columns=["status"]).head(20), use_container_width=True)

    # 🔹 6. Tabel Hasil Prediksi Lengkap
    st.markdown("### 📄 Hasil Prediksi Lengkap (20 Data Teratas)")
    st.dataframe(result_df.drop(columns=["status"]).head(20), use_container_width=True)

    # 🔹 7. Download CSV
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(result_df.drop(columns=["status"]))
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="hasil_klasifikasi.csv",
        mime="text/csv"
    )

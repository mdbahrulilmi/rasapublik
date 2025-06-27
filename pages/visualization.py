import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        st.subheader("📋 Tabel Evaluasi Lengkap")
        st.info("Tabel metrik seperti precision, recall, dan f1-score untuk setiap label.")
        st.dataframe(
            report_df.reset_index().rename(columns={"index": "Label"}).style.format(precision=3),
            use_container_width=True
        )

    with tab2:
        st.subheader("📊 Grafik Evaluasi per Label")
        st.info("Bar chart nilai precision, recall, dan f1-score untuk setiap label.")
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

    with tab3:
        st.subheader("🧱 Confusion Matrix")
        st.info("Matriks yang menunjukkan jumlah prediksi benar dan salah.")
        fig_cm = go.Figure(data=go.Heatmap(
            z=cm_df.values,
            x=cm_df.columns,
            y=cm_df.index,
            colorscale='Blues',
            showscale=True,
            hovertemplate="Prediksi: %{x}<br>Aktual: %{y}<br>Jumlah: %{z}<extra></extra>"
        ))
        fig_cm.update_layout(
            xaxis_title="Prediksi",
            yaxis_title="Aktual",
            title="Confusion Matrix",
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    with tab4:
        st.subheader("🥧 Distribusi Label yang Diprediksi")
        st.info("Pie chart distribusi hasil prediksi dari model.")
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

    with tab5:
        st.subheader("🧪 Uji Coba Prediksi Teks Baru")
        st.info("Masukkan teks baru untuk melihat prediksi model.")

        model = st.session_state.get("trained_model", None)
        vectorizer = st.session_state.get("vectorizer", None)
        label_encoder = st.session_state.get("label_encoder", None)
        select_kbest = st.session_state.get("select_kbest", None)

        if model and vectorizer and label_encoder and select_kbest:
            input_text = st.text_area("Masukkan teks:", height=100, placeholder="Contoh: Saya sangat puas dengan layanan ini.")

            if st.button("🔍 Prediksi"):
                if input_text.strip() == "":
                    st.warning("⚠️ Teks tidak boleh kosong.")
                else:
                    X_input = vectorizer.transform([input_text])
                    X_input_selected = select_kbest.transform(X_input)
                    y_pred = model.predict(X_input_selected)
                    label = label_encoder.inverse_transform(y_pred)[0]
                    st.success(f"📌 Hasil Prediksi: **{label}**")
        else:
            st.error("❌ Komponen model belum lengkap. Pastikan model telah dilatih.")


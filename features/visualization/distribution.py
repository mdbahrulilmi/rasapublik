import streamlit as st
import plotly.express as px

def tab(df):
    st.subheader("🥧 Distribusi Label yang Diprediksi")
    st.info("Pie chart distribusi hasil prediksi dari model.")
    pred_counts = df["predicted_label"].value_counts().reset_index()
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
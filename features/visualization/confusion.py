import streamlit as st
import plotly.graph_objects as go

def tab(df):
    st.subheader("🧱 Confusion Matrix")
    st.info("Matriks yang menunjukkan jumlah prediksi benar dan salah.")
    fig_cm = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=df.index,
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
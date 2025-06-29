import streamlit as st
import plotly.express as px

def tab(df): 
    st.subheader("📊 Grafik Evaluasi per Label")
    st.info("Bar chart nilai precision, recall, dan f1-score untuk setiap label.")
    metric_df = df.iloc[:-3][["precision", "recall", "f1-score"]].reset_index().rename(columns={'index': 'Label'})
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
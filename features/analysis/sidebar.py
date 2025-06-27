import streamlit as st
from features.analysis import start, svm, naivebayes

def option(data, name, text, label):
    st.sidebar.subheader('Metode Analisis Sentimen')
    method = st.sidebar.selectbox(
        'Pilih label otomatis',
        ("-","SVM","Naive Bayes"),
        label_visibility="collapsed"
        )
    submit = st.sidebar.button("Gunakan Metode",type="primary")

    if method == "-":
        start.option(data, name)
    if method == "SVM":
        svm.form(data)
    if method == "Naive Bayes":
        naivebayes.form(data)

    if submit:
        if method == "SVM":
            svm.algoritm(data, text, label)
        elif method == "Naive Bayes":
            naivebayes.algoritm(data, text, label)
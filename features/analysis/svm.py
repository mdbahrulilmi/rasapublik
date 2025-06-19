import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

def algoritm(df):
    # Tampilkan hanya progress spinner
    with st.spinner("🔄 Sedang melakukan analisis sentimen dengan SVM..."):

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            df['text'], df['label'], test_size=0.2, random_state=42, stratify=df['label'])

        # TF-IDF
        vectorizer = TfidfVectorizer()
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Model training
        model = SVC(class_weight='balanced')
        model.fit(X_train_vec, y_train)

        # Prediksi
        y_pred = model.predict(X_test_vec)

        # Evaluasi
        report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
        cm_df = pd.DataFrame(
            confusion_matrix(y_test, y_pred, labels=model.classes_),
            index=model.classes_, columns=model.classes_
        )

        # Hasil prediksi
        result_df = X_test.reset_index(drop=True).to_frame(name='text')
        result_df['actual_label'] = y_test.reset_index(drop=True)
        result_df['predicted_label'] = y_pred

        # Simpan hasil ke session_state untuk digunakan di halaman visualisasi
        st.session_state.visualisasi = {
            "classification_report": report_df,
            "confusion_matrix": cm_df,
            "hasil_prediksi": result_df
        }

    # Setelah proses selesai
    st.success("✅ Analisis selesai! Silakan buka tab *Visualisasi* untuk melihat hasil.")

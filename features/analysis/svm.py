import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE

def algoritm(df, text_col, label_col):
    with st.spinner("🔄 Sedang melakukan analisis sentimen dengan SVM..."):
        # 1. Label encoding
        y = df[label_col]
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # 2. TF-IDF vectorization dengan stopword tambahan
        extra_stopwords = ['tidak', 'sangat', 'sekali']
        tfidf = TfidfVectorizer(ngram_range=(1, 3), max_features=7000, stop_words=extra_stopwords)
        X = tfidf.fit_transform(df[text_col])

        # 3. Feature selection (chi2)
        X_selected = SelectKBest(chi2, k=3000).fit_transform(X, y_encoded)

        # 4. Resampling dengan SMOTE
        smote = SMOTE()
        X_resampled, y_resampled = smote.fit_resample(X_selected, y_encoded)

        # 5. Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
        )

        # 6. GridSearchCV untuk hyperparameter tuning
        params = {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale', 'auto']
        }
        grid = GridSearchCV(SVC(), params, cv=5, scoring='accuracy')
        grid.fit(X_train, y_train)

        best_params = grid.best_params_
        model = SVC(**best_params)
        model.fit(X_train, y_train)

        # 7. Prediksi
        y_pred = model.predict(X_test)

        # 8. Evaluasi
        report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
        cm_df = pd.DataFrame(
            confusion_matrix(y_test, y_pred),
            index=le.inverse_transform(sorted(set(y_test))),
            columns=le.inverse_transform(sorted(set(y_test)))
        )

        # 9. Hasil prediksi (tanpa teks asli karena sudah di-resample)
        result_df = pd.DataFrame({
            'actual_label': le.inverse_transform(y_test),
            'predicted_label': le.inverse_transform(y_pred)
        })

        # 10. Simpan ke session_state untuk tab visualisasi
        st.session_state.visualisasi = {
            "classification_report": report_df,
            "confusion_matrix": cm_df,
            "hasil_prediksi": result_df
        }

    st.success("✅ Analisis selesai! Silakan buka tab *Visualisasi* untuk melihat hasil.")

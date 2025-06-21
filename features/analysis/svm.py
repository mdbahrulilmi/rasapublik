import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE

def algoritm(df, text_col, label_col):
    with st.spinner("🔄 Sedang melakukan analisis sentimen dengan SVM..."):
        # 1. Encode label
        y = df[label_col]
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # 2. TF-IDF vektor dengan ngram (1,2) dan fitur 9000
        tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=9000)
        X = tfidf.fit_transform(df[text_col])

        # 3. Select top 4500 fitur (lebih ramping)
        X_selected = SelectKBest(chi2, k=4500).fit_transform(X, y_encoded)

        # 4. Resample dengan SMOTE
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X_selected, y_encoded)

        # 5. Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
        )

        # 6. GridSearch sederhana (cepat, fokus ke linear & rbf)
        params = {
            'C': [1, 10],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale']
        }

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid = GridSearchCV(SVC(), params, cv=cv, scoring='accuracy', n_jobs=-1)
        grid.fit(X_train, y_train)

        best_params = grid.best_params_
        model = SVC(**best_params)
        model.fit(X_train, y_train)

        # 7. Prediksi & Evaluasi
        y_pred = model.predict(X_test)
        report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
        cm_df = pd.DataFrame(
            confusion_matrix(y_test, y_pred),
            index=le.inverse_transform(sorted(set(y_test))),
            columns=le.inverse_transform(sorted(set(y_test)))
        )
        result_df = pd.DataFrame({
            'actual_label': le.inverse_transform(y_test),
            'predicted_label': le.inverse_transform(y_pred)
        })

        # 8. Simpan hasil ke Streamlit session
        st.session_state.visualisasi = {
            "classification_report": report_df,
            "confusion_matrix": cm_df,
            "hasil_prediksi": result_df,
            "best_params": best_params
        }

    st.success("✅ Analisis selesai! Efisien dan akurat. Silakan buka tab *Visualisasi*.")

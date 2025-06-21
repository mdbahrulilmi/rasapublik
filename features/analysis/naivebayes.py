import streamlit as st
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE

def algoritm(df, text_col, label_col):
    with st.spinner("🔄 Sedang melakukan pelatihan Naive Bayes..."):
        df[text_col] = df[text_col].astype(str)

        y = df[label_col]
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # 🔧 TF-IDF Stabil
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=15000,
            min_df=2,
            sublinear_tf=True
        )
        X = vectorizer.fit_transform(df[text_col])

        # 🔧 Select best 10000 fitur
        X_selected = SelectKBest(chi2, k=10000).fit_transform(X, y_encoded)

        # 🔧 Resample
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X_selected, y_encoded)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled, test_size=0.2, stratify=y_resampled, random_state=42
        )

        # Grid search stabil
        param_grid = {'alpha': [0.01, 0.03, 0.05, 0.1]}
        grid = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
        grid.fit(X_train, y_train)

        model = grid.best_estimator_
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

        st.session_state.visualisasi = {
            "classification_report": report_df,
            "confusion_matrix": cm_df,
            "hasil_prediksi": result_df,
            "best_params": grid.best_params_
        }

    st.success("✅ Naive Bayes selesai! Silakan buka tab *Visualisasi* untuk melihat hasil.")

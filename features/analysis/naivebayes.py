import streamlit as st
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE

def form(data):
    st.markdown("### 🧠 Naive Bayes")
    st.info("Silakan atur parameter di bawah untuk analisis sentimen.")

    with st.form("nb_form"):
        st.subheader("🔧 Pengaturan TF-IDF")
        ngram_range = st.slider("Pilih N-Gram Range", 1, 3, (1, 2))
        max_features = st.number_input("Jumlah maksimal fitur (TF-IDF)", value=15000, step=1000)

        st.subheader("🧪 Feature Selection")
        k_best = st.number_input("Jumlah fitur terpilih (SelectKBest)", value=10000, step=500)

        st.subheader("🧬 SMOTE Oversampling")
        smote_random_state = st.number_input("Random State untuk SMOTE", value=42)

        st.subheader("📊 Split Data")
        test_size = st.slider("Persentase Data Uji", 0.1, 0.5, 0.2, step=0.05)
        split_random_state = st.number_input("Random State Split", value=42)

        st.subheader("⚙️ Parameter GridSearchCV")
        alphas = st.multiselect("Alpha (Smoothing)", [0.01, 0.03, 0.05, 0.1, 0.5, 1.0], default=[0.01, 0.1])

        submitted = st.form_submit_button("✅ Simpan & Jalankan")

        if submitted:
            st.session_state.nb_settings = {
                "ngram_range": ngram_range,
                "max_features": max_features,
                "k_best": k_best,
                "smote_random_state": smote_random_state,
                "test_size": test_size,
                "split_random_state": split_random_state,
                "alpha": alphas
            }
            st.success("✅ Parameter disimpan. Silakan jalankan algoritma.")


def algoritm(df, text_col, label_col):
    if "nb_settings" not in st.session_state:
        st.warning("⚠️ Silakan isi dan simpan parameter terlebih dahulu.")
        return

    settings = st.session_state.nb_settings

    with st.spinner("🔄 Sedang melakukan analisis sentimen dengan Naive Bayes (TF-IDF + SelectKBest + SMOTE + GridSearchCV)..."):
        # Pastikan kolom teks bertipe string
        df[text_col] = df[text_col].astype(str)

        # Label encoding
        y = df[label_col]
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # TF-IDF
        tfidf = TfidfVectorizer(
            ngram_range=settings["ngram_range"],
            max_features=settings["max_features"],
            min_df=2,
            sublinear_tf=True
        )
        X = tfidf.fit_transform(df[text_col])

        # SelectKBest
        selector = SelectKBest(chi2, k=settings["k_best"])
        X_selected = selector.fit_transform(X, y_encoded)

        # SMOTE
        smote = SMOTE(random_state=settings["smote_random_state"])
        X_resampled, y_resampled = smote.fit_resample(X_selected, y_encoded)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled,
            test_size=settings["test_size"],
            random_state=settings["split_random_state"],
            stratify=y_resampled
        )

        # GridSearchCV on alpha
        param_grid = {'alpha': settings["alpha"]}
        grid = GridSearchCV(
            MultinomialNB(),
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1
        )
        grid.fit(X_train, y_train)

        # Best model
        best_params = grid.best_params_
        model = grid.best_estimator_
        y_pred = model.predict(X_test)

        # Hasil evaluasi
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

        # Simpan ke session
        st.session_state.visualisasi = {
            "classification_report": report_df,
            "confusion_matrix": cm_df,
            "hasil_prediksi": result_df,
            "best_params": best_params
        }
        st.session_state.trained_model = model
        st.session_state.vectorizer = tfidf
        st.session_state.label_encoder = le
        st.session_state.select_kbest = selector

    st.success("✅ Analisis selesai! Silakan cek tab *Visualisasi* untuk melihat hasil.")

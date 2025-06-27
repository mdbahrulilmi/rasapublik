import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE

def form(data):
    st.markdown("### 🧠 Support Vector Machine (SVM)")
    st.info("Silakan atur parameter di bawah untuk analisis sentimen.")

    with st.form("svm_form"):
        st.subheader("🔧 Pengaturan TF-IDF")
        ngram_range = st.slider("Pilih N-Gram Range", 1, 3, (1, 2))
        max_features = st.number_input("Jumlah maksimal fitur (TF-IDF)", value=9000, step=500)

        st.subheader("🧪 Feature Selection")
        k_best = st.number_input("Jumlah fitur terpilih (SelectKBest)", value=4500, step=100)

        st.subheader("🧬 SMOTE Oversampling")
        smote_random_state = st.number_input("Random State untuk SMOTE", value=42)

        st.subheader("📊 Split Data")
        test_size = st.slider("Persentase Data Uji", 0.1, 0.5, 0.2, step=0.05)
        split_random_state = st.number_input("Random State Split", value=42)

        st.subheader("⚙️ Parameter GridSearchCV")
        c_values = st.multiselect("C (Regulasi)", [0.1, 1, 10], default=[1, 10])
        kernels = st.multiselect("Kernel", ['linear', 'rbf', 'poly'], default=['linear', 'rbf'])
        gammas = st.multiselect("Gamma", ['scale', 'auto'], default=['scale'])

        submitted = st.form_submit_button("✅ Simpan & Jalankan")

        if submitted:
            st.session_state.svm_settings = {
                "ngram_range": ngram_range,
                "max_features": max_features,
                "k_best": k_best,
                "smote_random_state": smote_random_state,
                "test_size": test_size,
                "split_random_state": split_random_state,
                "C": c_values,
                "kernel": kernels,
                "gamma": gammas
            }
            st.success("✅ Parameter disimpan. Silakan jalankan algoritma.")

def algoritm(df, text_col, label_col):
    if "svm_settings" not in st.session_state:
        st.warning("⚠️ Silakan isi dan simpan parameter terlebih dahulu.")
        return

    settings = st.session_state.svm_settings

    with st.spinner("🔄 Sedang melakukan analisis sentimen dengan SVM..."):
        y = df[label_col]
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        tfidf = TfidfVectorizer(
            ngram_range=settings["ngram_range"],
            max_features=settings["max_features"]
        )
        X = tfidf.fit_transform(df[text_col])
        selector = SelectKBest(chi2, k=settings["k_best"])
        X_selected = selector.fit_transform(X, y_encoded)

        smote = SMOTE(random_state=settings["smote_random_state"])
        X_resampled, y_resampled = smote.fit_resample(X_selected, y_encoded)

        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled,
            test_size=settings["test_size"],
            random_state=settings["split_random_state"],
            stratify=y_resampled
        )

        params = {
            'C': settings["C"],
            'kernel': settings["kernel"],
            'gamma': settings["gamma"]
        }

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid = GridSearchCV(SVC(), params, cv=cv, scoring='accuracy', n_jobs=-1)
        grid.fit(X_train, y_train)

        best_params = grid.best_params_
        model = SVC(**best_params)
        model.fit(X_train, y_train)

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

        # ✅ Simpan ke session_state agar bisa dipakai di tab prediksi
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

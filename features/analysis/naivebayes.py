import streamlit as st
import pandas as pd
import re

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Siapkan stopwords dan stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Kamus normalisasi
kamus = {
    'gk': 'tidak', 'ga': 'tidak', 'bgt': 'banget', 'sy': 'saya',
    'tdk': 'tidak', 'sm': 'sama', 'tp': 'tapi', 'dr': 'dari',
    'jg': 'juga', 'aja': 'saja', 'udh': 'sudah', 'blm': 'belum',
    'dgn': 'dengan', 'trs': 'terus', 'krn': 'karena', 'udh': 'sudah'
}

# Normalisasi dan pembersihan teks
def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r'[^a-z\s]', '', teks)
    teks = re.sub(r'\s+', ' ', teks).strip()
    return teks

def normalisasi(teks):
    return ' '.join([kamus.get(kata, kata) for kata in teks.split()])

def hapus_stopwords_dan_stem(teks):
    return ' '.join([stemmer.stem(kata) for kata in teks.split() if kata not in stop_words])

# Fungsi utama
def algoritm(df, text_col, label_col):
    with st.spinner("🔄 Naikkan akurasi... sabar sebentar ya!"):
        # 1. Preprocessing
        df[text_col] = df[text_col].astype(str)
        df[text_col] = df[text_col].apply(bersihkan_teks).apply(normalisasi).apply(hapus_stopwords_dan_stem)

        # 2. Label encode
        y = df[label_col]
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # 3. TF-IDF optimal
        tfidf = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=15000,
            min_df=2,
            sublinear_tf=True
        )
        X = tfidf.fit_transform(df[text_col])

        # 4. Feature selection
        k_val = min(10000, X.shape[1])
        X_selected = SelectKBest(chi2, k=k_val).fit_transform(X, y_encoded)

        # 5. SMOTE
        smote = SMOTE()
        X_resampled, y_resampled = smote.fit_resample(X_selected, y_encoded)

        # 6. Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_resampled, y_resampled, test_size=0.2, stratify=y_resampled, random_state=42
        )

        # 7. GridSearch Naive Bayes
        param_grid = {'alpha': [0.01, 0.03, 0.05, 0.1, 0.3, 0.5, 1.0]}
        grid = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
        grid.fit(X_train, y_train)
        model = grid.best_estimator_

        # 8. Prediksi
        y_pred = model.predict(X_test)

        # 9. Evaluasi
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

        # 10. Simpan
        st.session_state.visualisasi = {
            "classification_report": report_df,
            "confusion_matrix": cm_df,
            "hasil_prediksi": result_df
        }

    st.success("✅ Selesai! Coba lihat hasilnya, ini udah dimaksimalkan.")

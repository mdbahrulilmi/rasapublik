import streamlit as st
import pandas as pd
import re
import os


def rule_based_label(text, positive_input, negative_input):
    positive = [w.strip().lower() for w in positive_input.split(',')]
    negative = [w.strip().lower() for w in negative_input.split(',')]

    words = re.findall(r'\b\w+\b', text.lower())

    pos_count = sum(word in words for word in positive)
    neg_count = sum(word in words for word in negative)

    if pos_count > 0 and neg_count == 0:
        return 'positif'
    elif neg_count > 0 and pos_count == 0:
        return 'negatif'
    elif pos_count == 0 and neg_count == 0:
        return 'netral'
    else:
        return 'positif' if pos_count > neg_count else 'negatif'


@st.dialog("Isi form dibawah ini", width="large")
def method(data, selected_column):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    positive_path = os.path.join(current_dir, "positive.txt")
    negative_path = os.path.join(current_dir, "negative.txt")

    try:
        with open(positive_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            default_positive = ", ".join([line.strip() for line in lines if line.strip()])
    except FileNotFoundError:
        default_positive = "bagus, mantap, cepat, puas, murah, recommended"

    try:
        with open(negative_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            default_negative = ", ".join([line.strip() for line in lines if line.strip()])
    except FileNotFoundError:
        default_negative = "nangis, lambat, jelek, mahal, kecewa"

    st.write("Masukkan kata kunci dan pisahkan dengan koma!")
    positive_input = st.text_area("Positif", value=default_positive)
    negative_input = st.text_area("Negatif", value=default_negative)

    if st.button("Submit Label"):
        df = data.copy()

        if 'label' not in df.columns:
            df['label'] = ""

        def apply_label(row):
            current_label = str(row['label']).strip().lower()
            if current_label in ["positif", "negatif", "netral"]:
                return current_label
            else:
                return rule_based_label(str(row[selected_column]), positive_input, negative_input)

        df['label'] = df.apply(apply_label, axis=1)
        df = df.iloc[:, -2:]
        df.columns = ['text', 'label']

        st.session_state["rulebased_labeled"] = df
        label_counts = df["label"].value_counts()

        st.write("### Jumlah Tiap Label:")
        st.write(f"✅ Positif: {label_counts.get('positif', 0)}")
        st.write(f"❌ Negatif: {label_counts.get('negatif', 0)}")
        st.write(f"➖ Netral : {label_counts.get('netral', 0)}")
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download hasil labeling",
            data=csv,
            file_name="hasil_rulebased.csv",
            mime="text/csv"
        )

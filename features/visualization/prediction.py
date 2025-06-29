import streamlit as st
from features.preprocessing import convert_negation, casefolding

def tab():
    st.subheader("🧪 Uji Coba Prediksi Teks Baru")
    st.info("Masukkan teks baru untuk melihat prediksi model.")

    model = st.session_state.get("trained_model", None)
    vectorizer = st.session_state.get("vectorizer", None)
    label_encoder = st.session_state.get("label_encoder", None)
    select_kbest = st.session_state.get("select_kbest", None)

    if model and vectorizer and label_encoder and select_kbest:
        input_text = st.text_area("Masukkan teks:", height=100, placeholder="Contoh: Saya sangat puas dengan layanan ini.")

        if st.button("🔍 Prediksi"):
            if input_text.strip() == "":
                st.warning("⚠️ Teks tidak boleh kosong.")
            else:
                negation_text = convert_negation.option(input_text)
                casefolded_text = casefolding.option(negation_text)
                X_input = vectorizer.transform([casefolded_text])
                X_input_selected = select_kbest.transform(X_input)
                y_pred = model.predict(X_input_selected)
                label = label_encoder.inverse_transform(y_pred)[0]
                st.success(f"📌 Hasil Prediksi: **{label}**")


    else:
        st.error("❌ Komponen model belum lengkap. Pastikan model telah dilatih dan disimpan di session_state.")

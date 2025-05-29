import streamlit as st

st.markdown("### Pilih dataset")

if "data_collection" in st.session_state and st.session_state.data_collection:
    dataset_names = [item["name"] for item in st.session_state.data_collection]

    selected_name = st.selectbox("Pilih Dataset:", dataset_names)

    selected_data = next(
        item["data"] for item in st.session_state.data_collection if item["name"] == selected_name
    )
    rows, cols = selected_data.shape
    st.write(f"Jumlah baris: {rows}")
    st.write(f"Jumlah kolom: {cols}")
    st.dataframe(selected_data.head())
    st.button("Simpan Data")
else:
    st.warning("Belum ada dataset yang disimpan.")

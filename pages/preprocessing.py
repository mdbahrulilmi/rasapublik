import streamlit as st
from features.preprocessing import missingvalues, casefolding

def main():
    st.markdown("### Pilih dataset")
    if "data_collection" in st.session_state and st.session_state.data_collection:
        dataset_names = [item["name"] for item in st.session_state.data_collection]
        selected_name = st.selectbox("Pilih Dataset:", dataset_names)
        selected_data = next(
            (item["data"] for item in st.session_state.data_collection if item["name"] == selected_name),
            None
        )   

    if selected_data is not None:
        if st.session_state.get("selected_data") is not selected_data:
            st.session_state["selected_data"] = selected_data

        rows, cols = selected_data.shape
        st.markdown(f"- Jumlah baris: {rows}  \n- Jumlah kolom: {cols}")
        cols = st.columns(5)
        for i, col_name in enumerate(selected_data.columns):
            col_index = i % 5
            with cols[col_index]:
                st.checkbox(label=col_name, key=f"{selected_name}_col_checkbox_{col_name}")
        selected_cols = [
            col_name for col_name in selected_data.columns
            if st.session_state.get(f"{selected_name}_col_checkbox_{col_name}", False)
        ]

        selected_only_data = selected_data[selected_cols]
        if len(selected_cols) > 0 :
            st.dataframe(selected_only_data.head())
            st.session_state['selected_only_data'] = selected_only_data
        else:
            return
    else:
        st.warning("Belum ada dataset yang disimpan.")

main()

if "selected_only_data" in st.session_state:
    data = st.session_state["selected_only_data"]

    st.button("Analisis Data")
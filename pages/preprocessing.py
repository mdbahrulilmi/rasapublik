import streamlit as st
from features.preprocessing import filter

def collection_data():
    if "data_collection" in st.session_state and st.session_state.data_collection:
        dataset_names = [item["name"] for item in st.session_state.data_collection]
        selected_name = st.selectbox("Pilih Dataset:", dataset_names)
        selected_data = next(
            (item["data"] for item in st.session_state.data_collection if item["name"] == selected_name)
        )
        return selected_data, selected_name

def main():
    st.markdown("### Pilih dataset")
    selected_data = None
    selected_name = None

    result = collection_data()
    if result:
        selected_data,selected_name = result

    if selected_data is not None:
        if st.session_state.get("selected_data") is not selected_data:
            st.session_state["selected_data"] = selected_data
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
            st.session_state['selected_only_data'] = selected_only_data
            st.session_state['selected_only_rows'], st.session_state['selected_only_cols'] = st.session_state['selected_only_data'].shape
        else:
            if 'selected_only_data' in st.session_state:
                del st.session_state['selected_only_data']

    else:
        st.warning("Belum ada dataset yang disimpan.")

main()

@st.dialog("Kasih datamu nama!")
def nameData(csv):
    if "filtered_data" in st.session_state:
        st.write(st.session_state['filtered_data'].shape)
    name = st.text_input("Nama Dataset")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f'{name}.csv',
        mime="text/csv",
        icon=":material/download:",
    )

only_data = None
if "selected_only_data" in st.session_state:

    only_data = st.session_state['selected_only_data']

    realTimeData = filter.option()

    realTimeRows, realTimeCols = realTimeData.shape
    st.markdown(f"- Jumlah baris: {realTimeRows}  \n- Jumlah kolom: {realTimeCols}")
    st.dataframe(realTimeData)

    if "filtered_data" in st.session_state:
        st.write(st.session_state['filtered_data'].shape)

    csv = realTimeData.to_csv().encode('utf-8')
    if st.button('Downlaod'):
        nameData(csv)
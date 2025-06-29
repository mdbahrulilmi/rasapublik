import streamlit as st

def option(data, selected_column):
    if 'start_index' not in st.session_state or 'amount' not in st.session_state:
        return

    label_options = ["Positif", "Netral", "Negatif"]

    start_index = st.session_state['start_index']
    amount = st.session_state['amount']
    end_index = min(start_index + amount, len(data))

    new_data_with_labels = []

    for i in range(start_index, end_index):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2], gap="medium")
        
        with col1:
            st.write(i+1)
        with col2:
            text = data[selected_column].iloc[i]
            current_label = ""

            if 'label' in data.columns:
                raw_label = data['label'].iloc[i]
                if isinstance(raw_label, str):
                    current_label = raw_label.strip().capitalize()

            if current_label:
                st.markdown(f"{text}")
            else:
                st.write(text)

        default_index = label_options.index(current_label) if current_label in label_options else 1

        with col3:
            option = st.selectbox(
                label=f"Label untuk data ke-{i}",
                label_visibility="collapsed",
                options=label_options,
                index=default_index,
                key=f"label_{i}",
                placeholder=f"Pilih label"
            )

        label = option
        new_data_with_labels.append({
            selected_column: data[selected_column].iloc[i],
            "label": label,
            "index": i
        })
        
    data_labeled = data.copy()
    if 'label' not in data_labeled.columns:
        data_labeled['label'] = ""

    for item in new_data_with_labels:
        idx = item['index']
        data_labeled.at[idx, 'label'] = item['label']

    if st.button('Simpan Label', type="primary"):
        st.session_state['data_labeled'] = data_labeled
        st.success("Label berhasil disimpan.")

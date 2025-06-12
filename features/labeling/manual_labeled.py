import streamlit as st

def option(data, selected_column):
    new_data_with_labels = []

    for i in range(st.session_state['amount']):
        col1, col2 = st.columns([0.7, 0.3], gap="medium",border=True)
        
        with col1:
            st.write(data[selected_column].iloc[i])
        with col2:
            option = st.selectbox(
                label=f"{i+1}",
                label_visibility="collapsed",
                options=["Positif", "Netral", "Negatif"],
                index=None,
                key=f"label_{i}",
                placeholder=f"Label ke-{i+1}"
            )
        new_data_with_labels.append({
            selected_column: data[selected_column].iloc[i],
            "label": option
        })

    data_labeled = data[[selected_column]].copy()
    data_labeled['label'] = ""
    for i in range(min(st.session_state['amount'], len(data_labeled))):
        data_labeled.at[data_labeled.index[i], 'label'] = new_data_with_labels[i]["label"]
    if st.button('Simpan Label', type="primary"):
        st.session_state['data_labeled'] = data_labeled
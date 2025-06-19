def option(data):
    min_count = data['label'].value_counts().min()
    
    balanced = (
        data.groupby('label', group_keys=False)
        .apply(lambda x: x.sample(n=min_count, random_state=42))
    )

    return balanced.sample(frac=1, random_state=42).reset_index(drop=True)
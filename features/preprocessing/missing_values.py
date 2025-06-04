def option(data):
    mv = data.isnull().any(axis=1).sum()
    data_clean = data.dropna()
    return data_clean, mv

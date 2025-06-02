def option(df):
    mv = df.isnull().any(axis=1).sum()
    df_clean = df.dropna()
    return df_clean, mv

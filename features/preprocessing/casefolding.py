import pandas as pd

def option(data):
    if isinstance(data, str):
        return data.casefold()
    elif isinstance(data, pd.Series):
        return data.fillna('').astype(str).apply(lambda x: x.casefold())
    elif isinstance(data, pd.DataFrame):
        return data.fillna('').astype(str).applymap(lambda x: x.casefold())
    else:
        raise TypeError("Input harus berupa str, pandas.Series, atau pandas.DataFrame")

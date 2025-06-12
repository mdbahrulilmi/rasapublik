import pandas as pd
import ast
import numpy as np

def option(data):
    # data = data.applymap(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.strip().startswith('[') else x)
    mask_nan = data.isnull().any(axis=1)
    mask_list_kosong = data.applymap(lambda x: isinstance(x, list) and len(x) == 0).any(axis=1)
    mask_drop = mask_nan | mask_list_kosong
    total_dihapus = mask_drop.sum()
    data_bersih = data[~mask_drop].reset_index(drop=True)

    return data_bersih, total_dihapus

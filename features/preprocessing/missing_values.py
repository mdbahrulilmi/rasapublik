import pandas as pd
import ast
import numpy as np

def option(data):
    # 1. Konversi semua string '[]' menjadi list Python kosong
    data = data.applymap(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.strip().startswith('[') else x)

    # 2. Cek missing values
    mask_nan = data.isnull().any(axis=1)

    # 3. Cek list kosong di kolom mana pun
    mask_list_kosong = data.applymap(lambda x: isinstance(x, list) and len(x) == 0).any(axis=1)

    # 4. Gabungkan semua kondisi
    mask_drop = mask_nan | mask_list_kosong

    # 5. Hitung berapa baris yang akan dihapus
    total_dihapus = mask_drop.sum()

    # 6. Buang baris-baris tersebut
    data_bersih = data[~mask_drop].reset_index(drop=True)

    return data_bersih, total_dihapus

def option(data):
    casefolded_series = data.fillna('').astype(str).applymap(lambda x: x.casefold())
    return casefolded_series
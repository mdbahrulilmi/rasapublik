from sklearn.feature_selection import SelectKBest, chi2

def option(X, y_encoded, k=10000):
    k_val = min(k, X.shape[1])
    selector = SelectKBest(chi2, k=k_val)
    X_selected = selector.fit_transform(X, y_encoded)
    return X_selected, selector
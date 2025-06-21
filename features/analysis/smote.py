from imblearn.over_sampling import SMOTE

def option(X, y, random_state=None):
    sm = SMOTE(random_state=random_state)
    X_res, y_res = sm.fit_resample(X, y)
    return X_res, y_res
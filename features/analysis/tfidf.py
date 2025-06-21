from sklearn.feature_extraction.text import TfidfVectorizer

def option(
    text_series,
    ngram=(1, 2),
    max_feat=10000,
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    norm='l2',
    stop_words=None
):
    tfidf = TfidfVectorizer(
        ngram_range=ngram,
        max_features=max_feat,
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=sublinear_tf,
        norm=norm,
        stop_words=stop_words
    )
    X = tfidf.fit_transform(text_series)
    return X, tfidf

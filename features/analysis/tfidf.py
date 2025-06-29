from sklearn.feature_extraction.text import TfidfVectorizer

def option(
    tokenized_series,
    ngram=(1, 2),
    max_feat=10000,
    min_df=1,
    max_df=1.0,
    sublinear_tf=True,
    norm='l2',
    stop_words=None
):
    def pisah_akhiran(tokens):
        modified = []
        for token in tokens:
            if token.endswith("kan") and len(token) > 5:
                modified.append(token[:-3])
                modified.append("kan2")
            elif token.endswith("an") and len(token) > 4:
                modified.append(token[:-2])
                modified.append("an2")
            elif token.endswith("i") and len(token) > 4:
                modified.append(token[:-1])
                modified.append("i2")
            else:
                modified.append(token)
        return ' '.join(modified)

    joined_text = tokenized_series.apply(pisah_akhiran)

    tfidf = TfidfVectorizer(
        ngram_range=ngram,
        max_features=max_feat,
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=sublinear_tf,
        norm=norm,
        stop_words=stop_words
    )

    X = tfidf.fit_transform(joined_text)
    return X, tfidf

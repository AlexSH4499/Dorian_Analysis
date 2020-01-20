import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidVectorizer
from sklearn.decomposition import TruncatedSVD


data = []

language = 'english'
stop_set = set(stopwords.words(language))

vectorizer = TfidVectorizer(stop_words = stop_set, use_idf=True, ngra_tange=(1,3))

X = vectorizer.fit_transform(data)#matrix with all docs and vals/freqs
comps_wanted = 27
lsa = TruncatedSVD(n_components=comps_wanted , n_iter=100)

lsa.fit(X)

lsa.components_[0]#first row for matrix V ^T (transponse)

#list of all the terms
terms = vectorizer.get_feature_names()

for i, comp in enumerate( lsa.components_):

    terms_in_comp = zip(temrs, comp)

    sorted_terms = sorted(terms_in_comp, key=lambda x:x[1], reverse=True)[:10]

    print(f"Concept {i}:")

    for term in sorted_terms:
        print(term[0])
    print()
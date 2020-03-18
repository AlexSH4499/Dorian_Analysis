
import typing

from typing import List, Any

import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

def extract_tokens(tweet_tuples):
    tokens_list = []

    for tweet_dict, classification in tweet_tuples:
        for key in tweet_dict.keys():#dict
            tokens_list.append(key)
    return tokens_list

def latent_semantic_analysis(data:List[Any]=[],language:str="english", num_comps:int=27 ):

    stop_set = set(stopwords.words(language))

    vectorizer = TfidfVectorizer(stop_words=stop_set, use_idf=True, ngram_range=(1,3)) 
    
    #loads all the data from the list onto the matrix, with words and their freqs
    text_data = extract_tokens(data)#tokens
    doc_matrix = vectorizer.fit_transform(text_data)

    lsa = TruncatedSVD(n_components=num_comps, n_iter=100)

    lsa.fit(doc_matrix)

    #first row for V ^(T) (transposed)
    #lsa.components_[0]

    terms = vectorizer.get_feature_names()

    for i , comp in enumerate(lsa.components_):
        term_in_comp = zip(terms, comp)

        #first 10 sorted terms only, for whatever reason
        sorted_terms = sorted(term_in_comp, key=lambda x:x[1], reverse=True)[:10]

        print(f"Concept[{i}]:\n\t")

        for term in sorted_terms:
            
            print(term)
            print(f"\t{term[0]}")

        print()
    
    return

# data = []

# language = 'english'
# stop_set = set(stopwords.words(language))

# vectorizer = TfidVectorizer(stop_words = stop_set, use_idf=True, ngra_tange=(1,3))

# X = vectorizer.fit_transform(data)#matrix with all docs and vals/freqs
# comps_wanted = 27
# lsa = TruncatedSVD(n_components=comps_wanted , n_iter=100)

# lsa.fit(X)

# lsa.components_[0]#first row for matrix V ^T (transponse)

# #list of all the terms
# terms = vectorizer.get_feature_names()

# for i, comp in enumerate( lsa.components_):

#     terms_in_comp = zip(terms, comp)

#     sorted_terms = sorted(terms_in_comp, key=lambda x:x[1], reverse=True)[:10]

#     print(f"Concept {i}:")

#     for term in sorted_terms:
#         print(term[0])
#     print()


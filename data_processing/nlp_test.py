
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.corpus import stopwords

from nltk import classify, NaiveBayesClassifier

#regex modules

import typing, random, re, string
from typing import List, Any

def twitter_regex()->List[str]:
    ignore = ['http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',#https/special chars
            '(@[A-Za-z0-9]+)',#handle
    ]
    return ignore

def filter_metadata(uncleandsed_tokens):

    cleansed_tokens = []
    for token, tag in pos_tag(uncleansed_tokens):

        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        if tag.startswith("NN"):
            pos = 'n'
        if tag.startswith("VB"):
            pos = 'v'
        else:
            pos='a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token,pos )

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleansed_tokens.append(token.lower())

    return cleansed_tokens


def filter_handles(uncleansed_tokens):

    cleansed_tokens = []
    for token, tag in pos_tag(uncleansed_tokens):

        token = re.sub("(@[A-Za-z0-9]+)","",token)
        if tag.startswith("NN"):
            pos = 'n'
        if tag.startswith("VB"):
            pos = 'v'
        else:
            pos='a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token,pos )

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleansed_tokens.append(token.lower())

    return cleansed_tokens

# def remove_noise(tweet_tokens:List[Any],  stop_words:tuple)->List[Any]:

#     cleaned_tokens = []

#     for token, tag in pos_tag(tweet_tokens):
#         #checks for http/https and special characters in token
#         # and replaces them with empty string
#         token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
#                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
#         #searches for handles and replaces them with empty string
#         token = re.sub("(@[A-Za-z0-9]+)","",token)

#         if tag.startswith("NN"):
#             pos = 'n'
#         if tag.startswith("VB"):
#             pos = 'v'
#         else:
#             pos='a'

#         lemmatizer = WordNetLemmatizer()
#         token = lemmatizer.lemmatize(token,pos )

#         if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
#             cleaned_tokens.append(token.lower())

#     return cleaned_tokens


def remove_noise(tweet_tokens:List[Any],  stop_words:tuple)->List[Any]:

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        #checks for http/https and special characters in token
        # and replaces them with empty string

        #apply all the regex filtering here
        for reg in twitter_regex():
            token = re.sub(reg,'', token)
        #searches for handles and replaces them with empty string
        #token = re.sub("(@[A-Za-z0-9]+)","",token)

        if tag.startswith("NN"):
            pos = 'n'
        if tag.startswith("VB"):
            pos = 'v'
        else:
            pos='a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token,pos )

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    return cleaned_tokens

#Remove conjugations of words like verbs
def lemmatize_sentence(tokens:List[Any])->List[Any]:

    lemmatizer = WordNetLemmatizer()

    lemmatized_sentence = []

    for word , tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos='v'
        else:
            pos='a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

#Generators
def get_all_words(cleaned_tokens_list):

    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):

    for tweet_token in cleaned_tokens_list:

        yield dict([token , True] for token in tweet_token)
#-----

def split_data(data_set:List[Any], cut_off_index:int=7000)->tuple:

    random.shuffle(data_set)
    train_data = data_set[:cut_off_index]
    test_data = data_set[cut_off_index:]
    return train_data, test_data

def test():
    #loading our pre-labeled data
    pos_tweets = twitter_samples.strings('positive_tweets.json')
    neg_tweets = twitter_samples.strings('negative_tweets.json')

    text = twitter_samples.strings('tweets.20150430-223406.json')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
    
    # print(tweet_tokens[0])
    #print(lemmatize_sentence(tweet_tokens[0]))
    stop_words = stopwords.words('english')#Words to ignore from English Language

    positive_cleaned_tokens_list = [remove_noise(tokens , stop_words) for tokens in positive_tweet_tokens]
    negative_cleaned_tokens_list = [remove_noise(tokens , stop_words) for tokens in negative_tweet_tokens]


    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    # print(remove_noise(tweet_tokens[0], stop_words))
    # print(positive_tweet_tokens[500])
    # print(positive_cleaned_tokens_list[500])

    pos_data = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
    neg_data = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]

    train, test = split_data(pos_data + neg_data, cut_off_index=7000)


    classifier = NaiveBayesClassifier.train(train)

    print(f"Accuracy is:{classify.accuracy(classifier, test)}")
    print(classifier.show_most_informative_features(10))
    return


if __name__ == "__main__":
    test()
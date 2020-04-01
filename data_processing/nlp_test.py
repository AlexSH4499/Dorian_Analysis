
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

from nltk import classify, NaiveBayesClassifier
from lsi import latent_semantic_analysis
from twitter_data_fetch import load_extracted_data
#regex modules

import typing, random, re, string
from typing import List, Any

def twitter_regex()->List[str]:
    '''
        Returns a list of all the regex we want to use to cleanse the tweets.
    '''
    ignore = ['http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',#https/special chars
            '(@[A-Za-z0-9]+)',#handle
    ]
    return ignore

def valid_token(stopwords , token):
    '''
        Verifies if token is valid by contrasting with the stopwords provided.
        Returns True if not found, otherwise False
    '''
    if len(token) > 0 and token not in string.punctuation and token.lower() not in stopwords:
        return True
    else:
        return False


def clean_token(token):
    for reg in twitter_regex():
        token = re.sub(reg,'', token)
    return token

def determine_pos(tag):
    '''
        Returns a simple character to indicate what a tag is.
        If pos is somehow left empty, the function will raise a value error for the unexpected tag.
        (noun) NN -> n
        (verb) VB -> v
        everything else -> a
    '''
    pos=''
    if tag.startswith("NN"):
            pos = 'n'
    if tag.startswith("VB"):
        pos = 'v'
    else:
        pos='a'

    if pos =='':
        raise ValueError('Sorry provided tag has unexpected value!')
    return pos

def remove_noise(tweet_tokens:List[Any],  stop_words:tuple)->Any:
    '''
        Receives a list of tokens extracted from the tweets and a list of stopwords to use for the filtering.
    '''
    clean_tokens = (WordNetLemmatizer().lemmatize(clean_token(token),determine_pos(tag)).lower() for token, tag in pos_tag(tweet_tokens) if valid_token(stop_words, token))
    return clean_tokens

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
def get_all_words(cleaned_tokens_list:List[Any]):

    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list:List[Any]):
    '''
        Creates a generator instance based off the provided cleansed tokens list.
        The generator yields a dict with k=token and value=True
    '''
    for tweet_token in cleaned_tokens_list:

        yield dict([token , True] for token in tweet_token)
#-----

def split_data(data_set:List[Any], cut_off_index:int=7000)->tuple:
    '''
        Splits a provided list into 2 separate lists based off a provided cut off index.

        Returns a pair of lists with cut-off point being the last element of the first and the inverse for the second list. 
    '''
    random.shuffle(data_set)
    train_data = data_set[:cut_off_index]
    test_data = data_set[cut_off_index:]
    return train_data, test_data

def prepare_data( tweets_data:List[str], language:str="english")-> List[Any]:
    '''
        Receives a list of text data extracted from tweets to be tokenized, lemmatized and left unclassified.
        Returns a list of tuples where value [0] is tweet_dict and value[1] is "Unclassified" string.
        Keyword arguments:
        
        tweets_data -- list of unprocessed text data to be tokenized and lemmatized
        language -- string representing the language whose stop words we want to use for tokenization
    '''
    #we
    #tokenize data
    #returns a list of tokens per tweet text provided
    tweet_tokens = [word_tokenize(tweet) for tweet in tweets_data ]

    #Words to ignore from Language
    stop_words = stopwords.words(language)

    cleaned_tokens_list = [remove_noise(tokens , stop_words) for tokens in tweet_tokens]

    #dict with token as keys and True as value
    tokens_for_model = get_tweets_for_model(cleaned_tokens_list)

    unclassified_data = [(tweet_dict, "Unclassified") for tweet_dict in tokens_for_model]

    return unclassified_data#list[tuple(tweet_dict,"classification")]

def prepare_test_data(language:str="english")-> List[Any]:
    '''
        Test  method with dummy data to use in a Naive Bayes Classifier
    '''

    data_set = []

    #raw data
    pos_tweets = twitter_samples.strings('positive_tweets.json')
    neg_tweets = twitter_samples.strings('negative_tweets.json')

    #tokenized data
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    #Words to ignore from Language
    stop_words = stopwords.words(language)

    positive_cleaned_tokens_list = [remove_noise(tokens , stop_words) for tokens in positive_tweet_tokens]
    negative_cleaned_tokens_list = [remove_noise(tokens , stop_words) for tokens in negative_tweet_tokens]


    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    pos_data = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
    neg_data = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]


    return pos_data + neg_data

# def load_tweets_csv(filename="tweets_data/test.csv"):

#     return

def test(language:str="english"):

    data_set = prepare_test_data(language)
    #7000 to train 3,000 to test
    train, test = split_data(data_set, cut_off_index=7000)


    classifier = NaiveBayesClassifier.train(train)

    print(f"Accuracy is:{classify.accuracy(classifier, test)}")
    print(classifier.show_most_informative_features(10))
    return

def test_lsi():

    latent_semantic_analysis(data=prepare_test_data(), language="english", num_comps=27)

if __name__ == "__main__":
    # test()
    test_lsi()
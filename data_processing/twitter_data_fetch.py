import tweepy, sys, json
from tweepy import *
from tweepy_au import *
from tweepy.models import Status

from csv_storage import *

class DorianStreamListener(tweepy.StreamListener):

    def __init__(self, output=sys.stdout):
        super(DorianStreamListener, self).__init__()
        self.output = output

    def on_data(self, data):
        print(data)
        return

    def on_status(self, status):
        print(status.text, file=self.output)

    def on_error(self, status_code):
        print(f'Error encountered:{status_code}\n')
        if status_code == 420:
            return False

        else:
            return True
    #context manager logic
    # def __enter__(self):

    #     return
    
    # def __exit__(self):

    #     return

def establish_stream( tracking="Dorian", num_tweets=10):
    
    auth = tweepy.AppAuthHandler(consumer_key=consumer_key,consumer_secret=consumer_secret)

    api = tweepy.API(auth)

    for tweet in tweepy.Cursor(api.search, q=tracking).items(num_tweets):
        print(tweet._json)#json format!

        yield tweet_to_json(tweet)#dict representation

#aUSELESS METHOD
#BUT I STILL WANT TO TRY AND MAKE IT USABLE

# def init_api():

#     auth ,stream = establish_stream()

#     try:
#         print("Stream Started")
#         # stream.sample(languages=['en'])
#     except KeyboardInterrupt:
#         print("Stopped")
    
#     finally:
#         print("Stream Ended")
#         # stream.disconnect()
#     return

def params():
    return ['id','user', 'place', 'lang','text']
    
def in_params(k):
    return k in params()

def clean_json(t_json):
    #there's a nested json dict in 'user'
    #this is the user data layout in the nested json
    user_dict = t_json['user']
    res = {}
    for k , v in t_json.items():
        if in_params(k):
            if k == 'user':
                res[k] = user_dict['screen_name']
            else:
                if v == None:
                    res[k] = 'NAN'
                else:
                    res[k] = v
    return res

def tweet_to_json(tweet):
    return tweet._json#thiw was not specified in the documentation but is in the class of the Status Object


def fetch_data(filename='tweets_data/test.csv'):
    #establish a connection
    #receive and parse the tweets into the format we want
    #pass parsed tweets into the csv file we want

    tweet_dicts  = [clean_json(tweet_json)
                     for tweet_json  in
                      establish_stream(num_tweets=100)]

    create_file(data=tweet_dicts, fieldnames=params() ,name=filename)

    return

if __name__ == '__main__':
    fetch_data()
    
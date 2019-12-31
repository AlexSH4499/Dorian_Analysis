import tweepy, sys
from tweepy_au import *

# consumer_key, consumer_secret = "KEY HERE", "SECRET HERE"
# access_token, access_token_secret = "token here" ,"secret token here"

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# public_tweets = api.home_timeline()

# for tweet in public_tweets:
#     print(tweet.text)


class DorianStreamListener(tweepy.StreamListener):

    def __init__(self, output=sys.stdout):
        super(DorianStreamListener, self).__init__()
        self.output = output

    def on_status(self, status):
        print(status.text, file=self.output)

    def on_error(self, status_code):
        print(f'Error encountered:{status_code}')
        if status_code == 420:
            return False

        else:
            return True

def establish_stream(consumer_key=consumer_key, consumer_secret=consumer_key, tracking="Dorian"):
    
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    stream_listener = DorianStreamListener()
    stream_listener = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream_listener.filter(track=tracking, is_async=True)#will run on its own independent thread

    return  auth, stream_listener

def init_api():

    auth ,stream = establish_stream()

    try:
        print("Stream Started")
        stream.sample(languages=['en'])
    except KeyboardInterrupt:
        print("Stopped")
    
    finally:
        print("Stream Ended")
        stream.disconnect()
        
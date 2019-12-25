import tweepy

# consumer_key, consumer_secret = "KEY HERE", "SECRET HERE"
# access_token, access_token_secret = "token here" ,"secret token here"

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# public_tweets = api.home_timeline()

# for tweet in public_tweets:
#     print(tweet.text)


class DorianStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

        else:
            return True

def establish_stream(consumer_key, consumer_secret, tracking="Dorian"):
    
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

    stream_listener = DorianStreamListener()
    stream_listener = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream_listener.filter(track=tracking, is_async=True)#will run on its own independent thread

    return stream_listener
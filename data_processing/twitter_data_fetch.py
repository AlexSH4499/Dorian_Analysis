import tweepy

consumer_key, consumer_secret = "KEY HERE", "SECRET HERE"
access_token, access_token_secret = "token here" ,"secret token here"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)
import tweepy, sys, json
from tweepy import *
from tweepy_au import *
from tweepy.models import Status

from csv_storage import *
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

    def __enter__(self):

        return
    
    def __exit__(self):

        return

def establish_stream( tracking="Dorian", num_tweets=10):
    
    auth = tweepy.AppAuthHandler(consumer_key=consumer_key,consumer_secret=consumer_secret)
    # auth = OAuthHandler(consumer_key,consumer_secret)
    # auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # try:
    #     redirect_url = auth.get_authorization_url()
    #     session.set('request_token', auth.request_token['oath_toekn'])
    # except tweepy.TweepError:
    #     print('Error: Failed to acquire request token.')

    api = tweepy.API(auth)
    # api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # stream_listener = DorianStreamListener()
    # stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    # stream.filter(track=tracking, is_async=True)#will run on its own independent thread

    # return  auth, stream
    for tweet in tweepy.Cursor(api.search, q=tracking).items(num_tweets):
        # print(tweet.parse(api, json=))
        print(tweet._json)#json format!
        # print(type(tweet._json))#json format!
        # # print(type(tweet))
        # print()
        yield tweet_to_json(tweet)#dict representation
        #print(tweet.text)
    #return auth, 0

def init_api():

    auth ,stream = establish_stream()

    try:
        print("Stream Started")
        # stream.sample(languages=['en'])
    except KeyboardInterrupt:
        print("Stopped")
    
    finally:
        print("Stream Ended")
        # stream.disconnect()
    return

def params():
    return ['id','user', 'place', 'lang','text']
    
def in_params(k):
    return k in params()

def clean_json(t_json):
    #there's a nested json dict in 'user'
    #this is the user data layout in the nested json
    #"{'id': 1048783914,
    #  'id_str': '1048783914',
    #  'name': 'Dallas Mavs France',
    #  'screen_name': 'DallasMavsFr',
    #  'location': 'Würzburg, TX, Slovenia ',
    #  'description': ""Compte français d'une équipe sympatoche, emmenée par un prodige comme on en voit qu'une fois tous les 20 ans mais aussi par Luka Dončić.        2011 🏆 & Dirk💍"",
    #  'url': 'https://t.co/5M4RAsAQrB',
    #  'entities': {'url': {
    #                       'urls': [
    # 
    #                               {'url': 'https://t.co/5M4RAsAQrB',
    #                                'expanded_url': 'http://www.youtube.com/c/DallasMavsFrance',
    #                                'display_url': 'youtube.com/c/DallasMavsFr…',
    #                                    'indices': [0, 23]
    #                               }]
    #                       },
    #  'description': {'urls': []}},
    #  'protected': False,
    #  'followers_count': 18004,
    #  'friends_count': 367, 
    # 'listed_count': 133,
    #  'created_at': 'Sun Dec 30 20:53:11 +0000 2012',
    #  'favourites_count': 20719, 'utc_offset': None,
    #  'time_zone': None,
    #  'geo_enabled': True, 
    # 'verified': False, 
    # 'statuses_count': 46595,
    #  'lang': None, 
    # 'contributors_enabled': False,
    #  'is_translator': False,
    #  'is_translation_enabled': False, 
    # 'profile_background_color': '000000',
    #  'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png',
    #  'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png',
    #  'profile_background_tile': False,
    #  'profile_image_url': 'http://pbs.twimg.com/profile_images/1136469954998558725/3WT5aB7y_normal.jpg',
    #  'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1136469954998558725/3WT5aB7y_normal.jpg',
    #  'profile_banner_url': 'https://pbs.twimg.com/profile_banners/1048783914/1576137182',
    #  'profile_link_color': '1B95E0', 'profile_sidebar_border_color': '000000',
    # 'profile_sidebar_fill_color': '000000',
    #  'profile_text_color': '000000',
    #  'profile_use_background_image': False,
    #  'has_extended_profile': True, 
    # 'default_profile': False,
    #  'default_profile_image': False,
    #  'following': None,
    #  'follow_request_sent': None,
    #  'notifications': None,
    #  'translator_type': 'none'}"
    user_dict = t_json['user']
    # print(user_dict['screen_name'])
    res = {}
    for k , v in t_json.items():
        if in_params(k):
            if k == 'user':
                res[k] = user_dict['screen_name']
            else:
                if v == None or v.strip()=="":
                    res[k] = 'NAN'
                else:
                    res[k] = v
    # print(type(t_json['user']))
    # user_nested = json.loads(t_json['user'])
    # print(user_nested)
    # return {k:v for k , v in t_json.items() if in_params(k) and k != 'user':
    #                                         elif k == 'user':
    #                                              v = user_dict['screen_name']}
    return res

def tweet_to_json(tweet):
    return tweet._json


def fetch_data(filename='test.csv'):
    #establish a connection
    #receive and parse the tweets into the format we want
    #pass parsed tweets into the csv file we want

    tweet_dicts  = [clean_json(tweet_json)
                     for tweet_json  in
                      establish_stream(num_tweets=1)]

    create_file(data=tweet_dicts, fieldnames=params() ,name=filename)

    return

if __name__ == '__main__':
    fetch_data()
    #
    # init_api()
    
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
    # return ['status_id','user_id ', 'place', 'lang','text']
    return ['status_id','user_id ','created_at', 'place_name','place_fullname', 'country' ,'location', 'retweet_location', 'geo_coords', 'coords_coords', 'bbox_coords', 'place', 'lang','text']

    
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


# def extract_data_csv(filepath=default_csv_file ,date_time=""):#the constant is defined on a file not included in this project
#     csv_dic_gen  = load_file(name=filepath)#generator for dictionaries containing the data

#     li_dics=({k : v for k , v in dic.items() if in_params(k)} for dic in csv_dic_gen)

#     print(type(li_dics))
#     # li_dics = []
#     # for dic in csv_data:
#         # temp_dic = {}
#         # for k , v in dic:
#         #     if in_params(k):
#         #         temp_dic[k] = v
#         # li_dics.append(temp_dic)

#     # print(li_dics[0].keys())

#     # for row in csv_data:
#     #     print(f'Length of Row:{len(row)}\n Row Contents:{row}\n\n')
#     # filtered_data = { k:v for k,v in csv_data if in_params(k)} #filtered the params we want, now we have to fix the values
#     return return li_dics

def extract_data_csv(filepath=default_csv_file ,date_time=""):#the constant is defined on a file not included in this project
    return ({k : v for k , v in dic.items() if in_params(k)} for dic in load_file(name=filepath))

if __name__ == '__main__':
    # fetch_data()
    for dic in extract_data_csv():
        print(dic)
        print()
    
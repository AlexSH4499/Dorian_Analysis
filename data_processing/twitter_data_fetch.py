import typing
from typing import List, Any, Dict
import tweepy, sys, json
from tweepy import *
from tweepy_au import *
from tweepy.models import Status

import re
from csv_storage import *
import numpy as np


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


def establish_stream( tracking:str="Dorian", num_tweets:int=10):
    
    auth = tweepy.AppAuthHandler(consumer_key=consumer_key,consumer_secret=consumer_secret)

    api = tweepy.API(auth)

    for tweet in tweepy.Cursor(api.search, q=tracking).items(num_tweets):
        print(tweet._json)#json format!

        yield tweet_to_json(tweet)#dict representation

#aUSELESS METHOD
#BUT I STILL WANT TO TRY AND MAKE IT USABLE

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

def params()->List[str]:
    return ['status_id','user_id ','created_at',
    'place_name','place_fullname', 'country' ,
    'location', 'retweet_location',
    'geo_coords', 'coords_coords', 'bbox_coords', 'place', 'lang','text']

    
def in_params(k:str)->bool:
    return k in params()

# Put any as second param because IDK right now
def clean_json(t_json:Dict[str,Any])->Dict[str, Any]:
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
    if tweet._json == None:
        raise ValueError("Tweet does not contain a valid json instance.\n")
    return tweet._json#this was not specified in the documentation but is in the class of the Status Object

#We need to fix this
# should detect if there is a NA or repetitions of it
# so we only pick the most important non-NA location value is kept
def extract_location_data(tweet):
    expression = "^([N][A])+$"#need to fix this so it detects NAN better from twitter's API
    pattern = re.compile(expression)
    possible_locations= ['location', 'retweet_location', 'geo_coords', 'coords_coords', 'bbox_coords', 'place_fullname', 'place_name', 'place', 'country' ,]
    ans=''

    for loc in possible_locations:

        if tweet[loc].strip().split().join() != None:

            if len(pattern.search(tweet[loc]).group())  >  0:#should check if it contains this in a substring using regex
                ans = np.nan
                break
            else:
                ans = loc
                break
    if ans == '':
        ans = np.nan

    return ans

def fetch_data(filename:str='tweets_data/test.csv'):
    #establish a connection
    #receive and parse the tweets into the format we want
    #pass parsed tweets into the csv file we want

    tweet_dicts  = [clean_json(tweet_json)
                     for tweet_json  in
                      establish_stream(num_tweets=100)]

    create_file(data=tweet_dicts, fieldnames=params() ,name=filename)

    return


def extract_data_csv(filepath=default_csv_file ,date_time=""):#the constant is defined on a file not included in this project
    '''
    generator that yields dictionaries from the filepath provided
    '''
    return ({k : v for k , v in dic.items() if in_params(k)} for dic in load_file(name=filepath))

def format_datetime(data:List[Dict[str,str]])->Dict[str,str]:
    to_extract="created_at"#key we want to extract and format

    for dic in data:

        datetime= dic[to_extract]# YYYY/MM/DD hh:mm:ss
        del dic[to_extract]#remove the dic entry that has both stored inline

        # wasnt saving the changes to datetime var, derp
        datetime = datetime.strip()
        datetime = datetime.split(' ')

        # This is not splitting appropriately
        dic['date'] = datetime[0]
        dic['time'] = datetime[1]

    return data

#Figured out the problem, ws trying to iterate over an already used generator
#refer to iter == iter problem in python
def save_extracted_data(data:List[Dict[str,str]]=[dic for dic in extract_data_csv()], filename:str="extracted_harp.csv"):
    try:
        param =params()
        param.remove("created_at")
        param.append("date")
        param.append("time")

        create_file(data= format_datetime(data), fieldnames=param,name=filename)
    except FileExistsError as e:
        print(f"Sorry the file [{filename}] already exists...\n{e}\n\n")
    
    finally:
        print(f"\n[!]Finished saving extracted data into {filename}\n\n")

    return

# TODO: FILTER OUT THE NAN Data from location value
def load_extracted_data(filename:str='tweets_data/test.csv', filter_params:List[str]=['text',''])->List[Dict[str,str]]:

    data = load_file(name=filename)#list of dics
    extracted=[]
    for dic in data:

        #here we can filter the data we want only
        # for k in dic.keys():
        #     if k == 'place':

        #         if dic[k] == 'NAN':
        #             continue
        # else:
        extracted.append(dic['text'])


    return data

if __name__ == '__main__':
    # fetch_data()
    # for dic in extract_data_csv():
    #     print(dic)
    #     print()
    save_extracted_data()
    
import csv
from collections import OrderedDict


#might need to re-think what data format will be in
#should obviously be a dict

def create_file(data=[], fieldnames=[] ,name="",delimiter=','):

    with open(name, 'w') as csv_file:

        wr = csv.DictWriter(csv_file, fieldnames=fieldnames )
        wr.writeheader()

        for row in data:
            wr.writerow(row)


def load_file(name=''):
    
    with open(name, newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            yield row

class TweetDict:

    #data we want to store (in a tuple)
    # def __init__(self,user='',geo_loc='',text_data= '', ):
    def __init__(self,tweet_data=tuple() ):
        assert len(tweet_data) == len(self.params())
        self.dic = OrderedDict(zip(self.params(), tweet_data))
        # assert len(tweet_data) == len(self.params())
        # for par,val in zip(self.params(), tweet_data):
        #     self.dic[par] = val
        return

    def data(self):
        return (self.dic[param] for param in self.params())

    #parameters we want to store
    def params(self):
        params=('id','user', 'place', 'lang','text_data')
        return params
    
    #TODO:adds a ',' at the end, should not be the case needs to be fixed
    def __str__(self):
        st_rep = ""

        for arg, val in self.dic.items():
            st_rep += f'{val},'
        st_rep= st_rep[0:len(st_rep)-2]#removes last comma
        return st_rep
    
    #so we can reuse the same object instead of recreating it always
    def reset(self):

        for k,v in self.dic:
            self.dic.popitem()
    
        return
    
    def recycle(self, new_tweet_data=tuple()):
        #TODO:make sure the dictionary
        #    :doesn't keep
        #    :garbage stored from previous tweet
        assert len(new_tweet_data) == len(self.params())
        for k,v in zip(self.params() , new_tweet_data):
            self.dic[k] = v 
        return





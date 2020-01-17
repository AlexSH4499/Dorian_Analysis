import csv
from collections import OrderedDict


#might need to re-think what data format will be in
#should obviously be a dict

def create_file(data=[], fieldnames=[] ,name="",delimiter=','):
    print(data)
    try:
        with open(name, mode='w') as csv_file:

            wr = csv.DictWriter(csv_file, fieldnames=fieldnames )
            wr.writeheader()

            for row in data:
                wr.writerow(row)
    except IOError as e:
        print(f'Error while creating file: {name}',e)

def load_file(name=''):
    
    try:
        with open(name, newline="", mode='r') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                yield row
    except IOError as e:
        print(f'Error while loading file: {name}', e)


#this seems unnecessary
class TweetData:

    def __init__(self,desired_data):
        self.data = desired_data
        return
    
    
    


class TweetDict(OrderedDict):

    #data we want to store (in a tuple)
    def __init__(self,tweet_json:{}):
        # assert len(tweet_data) == len(self.params())
        self.dic = OrderedDict()
        self.validate(tweet_json)
        # assert len(self.dic) == len(self.params()
        

    def data(self):
        return (self.dic[param] for param in self.params())

    #parameters we want to store
    def params(self):
        params=('id','user', 'place', 'lang','text')
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

    def validate(self, incoming_dict:{}):
        parms = self.params()#the data we actually want to extract

        for param in parms:
            try:
                self.dic[param] = incoming_dict[param]
            except Exception as e:
                print(f"Invalid Key:{param} val:{incoming_dict[param]}", e)
        return

def test():
    dic = dict(zip(('id','user', 'place', 'lang','text_data'),(0,1, 10 , 'eng', 'assignment')))
    dat=[]
    dat.append(dic)
    create_file(name='test.csv',data=dat, fieldnames=['id','user', 'place', 'lang','text_data'] )

    return

if __name__ == '__main__':
    test()
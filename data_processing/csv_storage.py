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

class TweetDict(OrderedDict):

    def __init__(self,user='',geo_loc='',text_data= '', ):
        self.dic = OrderedDict()
        self.dic['user']=user
        self.dic['geo_loc']= geo_loc
        self.dic['text_data']=text_data
        return

    def params(self):
        return self.dic.keys()
    
    def __str__(self):

        return f"[{self.dic['user']}]@{self.dic['geo_loc']= geo_loc}| {self.dic['text_data']=text_data} |"




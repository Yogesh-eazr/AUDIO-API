import pandas as pd
import numpy as np
import pymongo

from bson import json_util

import json
from flask import jsonify, request, Flask

conn = pymongo.MongoClient('localhost',27017)
db = conn['SONGS_APIDB']
collection = db['songs_list']

t = db.songs_list

app = Flask(__name__)


### using datetime
from datetime import date, time, datetime
date(year=2020, month=1, day=31)
mm = str(datetime(year=2021, month=3, day=31, hour=1, minute=14, second=31))
nn = str(datetime(year=2021, month=4, day=6, hour=3, minute=14, second=31))
oo = str(datetime(year=2021, month=5, day=12, hour=4, minute=14, second=31))
pp = str(datetime(year=2021, month=6, day=25, hour=5, minute=14, second=31))
qq = str(datetime(year=2021, month=7, day=3, hour=6, minute=14, second=31))
rr = str(datetime(year=2021, month=8, day=1, hour=7, minute=14, second=31))

### created a song dataset
song_field = {'ID':['1','2','3','4','5','6'],'name':['bole','chudiyan','high rated','gabru','jis desh me','dilbar'],'duration_in_seconds':['258','451','331','245','651','466'],'uploaded_time':[mm,nn,oo,pp,qq,rr]}

song_data_frame = pd.DataFrame(song_field)

song_dict = {}
for i in range(len(song_data_frame['ID'])):
    mk = song_data_frame['ID'][i]

    song_dict[mk] = list([song_data_frame['name'][i],int(song_data_frame['duration_in_seconds'][int(i)]),song_data_frame['uploaded_time'][i]])

print(song_dict)

def correct_encoding(dictionary):

    new = {}
    for key1, val1 in dictionary.items():
        # Nested dictionaries
        if isinstance(val1, dict):
            val1 = correct_encoding(val1)

        if isinstance(val1, np.bool_):
            val1 = bool(val1)

        if isinstance(val1, np.int64):
            val1 = int(val1)

        if isinstance(val1, np.float64):
            val1 = float(val1)

        new[key1] = val1

    return new

new_one = correct_encoding(song_dict)

print(new_one)

### insert into table

collection.insert(new_one,check_keys=False)
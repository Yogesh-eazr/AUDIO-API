from flask import jsonify, request, Flask, Response
import pymongo
import json
from bson import ObjectId, json_util
from datetime import datetime
conn = pymongo.MongoClient('localhost',27017)
db = conn['SONGS_APIDB']
t = db.songs_list

app = Flask(__name__)


### GET method
@app.route("/Song", methods = ['GET'])
def getSong():
    try:
        newkey_list = []
        for t1 in t.find():
            newkey_list.append(t1)
        print(len(newkey_list))
        print(newkey_list)
        for i in range(len(newkey_list)):
            return json.loads(json_util.dumps(newkey_list[i]))
    except:
        return Response(response= json.dumps({"MSG":"NO DATA FOUND"}))


### update method
@app.route("/Song", methods=['POST'])
def mongoPythonPost():
    newkey_list = []
    da = request.get_json()
    data = da['add_song']
    for t1 in t.find():
        mm = len(t1.keys())
        newkey_list.append(t1)
    bb = mm
    nm = newkey_list[0]
    nm[f'{bb}'] = data
    gh = nm['_id']
    print(newkey_list[0])
    print(len(newkey_list))
    t.update_one({"_id": ObjectId(f"{gh}")}, {'$set': {f'{bb}': data}})

    #### try and except method is to avoid TypeError: Object of type ObjectId is not JSON serializable
    try:
        return jsonify({"mm": newkey_list[0]})
    except:
        return json.loads(json_util.dumps(newkey_list[0]))

#### delete api
@app.route("/Song/<id>", methods= ['DELETE'])
def deleteSong(id):
    for t1 in t.find({"_id":ObjectId(id)}):
        m = t1["_id"]
        try:
            t.delete_one({"_id": ObjectId(m)})
            return Response(response=json.dumps({"MSG": "user deleted"}),status=200)
        except:
            return Response(response=json.dumps({"MSG": "user not deleted"}),status=500)

#### create method.
@app.route("/Song/Create", methods = ['POST'])
def createSong():
    da = request.get_json()
    for t1 in t.find():
        mm = len(t1.keys())
    data = da['add_song']

    ### date validation
    date_check = data[2]
    split_date = date_check.split("-")
    sum_date = (int(split_date[0])*1000) + (int(split_date[1])*100) + int(split_date[2])
    now_date = datetime.now()
    now_year = int(now_date.year) * 1000
    now_month = int(now_date.month) * 100
    now_day = int(now_date.day)
    now_date_sum = now_month + now_year + now_day
    bb = str(mm)
    new_dct = {}
    new_dct[bb] = data
    try:
        if (now_date_sum <= sum_date):
            t.insert(new_dct,check_keys = False)
            return Response(response=json.dumps({"MSG":"SONG CREATED"}))
        else:
            return Response(response=json.dumps({"MSG":"DATE of UpLOAD IS INVALID"}))
    except:
        return Response(response=json.dumps({"MSG":"SONG NOT CREATED"}))

if __name__=='__main__':
    app.run('localhost', 8080)
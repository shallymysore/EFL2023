from flask import Flask,make_response,request
from pymongo import MongoClient
import random
from bson import json_util,ObjectId
import json

app = Flask(__name__)

client = MongoClient("mongodb+srv://efladmin:god_is_watching@cluster0.eezohvz.mongodb.net/?retryWrites=true&w=majority")

db=client["efl2023"]

collections = db["eflCricket"]

@app.route("/")
def welcome():
    return "Welcome to EFL2023"

@app.route('/getplayer', methods=["GET"])
def get_player():
    tier1 = []
    tier2 = []
    tier3 = []
    tier4 = []
    cursor = collections.find()
    for item in cursor:
        if item['tier'] == 1 and item['status']=="unsold":
            tier1.append(item)
        elif item['tier'] == 2 and item['status']=="unsold":
            tier2.append(item)
        elif item['tier'] == 3 and item['status']=="unsold":
            tier3.append(item)
        elif item['tier'] == 4 and item['status']=="unsold":
            tier4.append(item)
    if len(tier1) > 0:
        pick = random.choice(tier1)
    elif len(tier2) > 0:
        pick = random.choice(tier2)
    elif len(tier3) > 0:
        pick =random.choice(tier3)
    elif len(tier4) > 0:
        pick =random.choice(tier4)
    else:
        print("All players are processed")
    
    return json.loads(json_util.dumps(pick))

@app.route('/updateplayer/<_id>',methods=['PUT'])
def update_player(_id):

    updated_data = request.get_json()
    
    filter = {"_id": ObjectId(str(_id))}
   
    result = collections.update_one(filter, {"$set": updated_data})
   
    return json_util.dumps(result.raw_result)

if __name__ == '__main__':
    app.run()
    

from flask import Flask,make_response,request
from pymongo import MongoClient
import random
from bson import json_util,ObjectId
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb+srv://efladmin:god_is_watching@cluster0.eezohvz.mongodb.net/?retryWrites=true&w=majority")

db=client["efl2023"]

collections = db["eflCricket"]

ownercollection = db["eflCricketOwners"]

@app.route("/")
def welcome():
    return "Welcome to EFL2023"

@app.route('/getallplayers', methods=["GET"])
def get_all_players():
    players = []
    cursor = collections.find()
    for player in cursor:
        players.append(player)
    return json.loads(json_util.dumps(players))

@app.route('/getallownersdata', methods=["GET"])
def get_all_owners():
    owners = []
    cursor = ownercollection.find()
    for owner in cursor:
        owners.append(owner)
    return json.loads(json_util.dumps(owners))

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
    
    #code to handle second owner update
    if updated_data['status'] == "sold":
        owner_team = updated_data['ownerTeam']

        myquery = {"ownerName":owner_team}

        owners_data = ownercollection.find(myquery)

        for owner_items in owners_data:
            owner_items["currentPurse"] = owner_items["currentPurse"] - int(updated_data["boughtFor"])
            owner_items["totalCount"] = owner_items["totalCount"] + 1
            owner_items["maxBid"] = owner_items["currentPurse"] - (35 * (15-owner_items["totalCount"]))
            if updated_data["role"] == "Batter":
                owner_items["batCount"] = owner_items["batCount"] + 1
            elif updated_data["role"] == "Bowler":
                owner_items["ballCount"] = owner_items["ballCount"] + 1
            elif updated_data["role"] == "Allrounder":
                owner_items["batCount"] = owner_items["batCount"] + 1
                owner_items["ballCount"] = owner_items["ballCount"] + 1
            elif updated_data["role"] == "WK-Batter":
                owner_items["batCount"] = owner_items["batCount"] + 1
                owner_items["wkCount"] = owner_items["wkCount"] + 1
            else:
                print("Role not found")
            
            if updated_data["country"] != "India":
                owner_items["fCount"] = owner_items["fCount"] + 1

        filter_owner = {"_id": ObjectId(str(owner_items["_id"]))}
        result_owner = ownercollection.update_one(filter_owner, {"$set": owner_items})
   
    return json_util.dumps(result.raw_result)

if __name__ == '__main__':
    app.run()
    

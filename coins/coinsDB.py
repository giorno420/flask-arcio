import pymongo


cluster = pymongo.MongoClient("mongodb+srv://YOUR_MONGO_USERNAME:YOUR_MONGO_PASSWORD@YOUR_MONGO_CLUSTER.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE")
db = cluster["CLUSTER_NAME"]
coinsCluster = db.userdata

def addCoins(userID):
    userID = int(userID)
    coinsCluster.update_one({"_id": userID}, {"$inc": {"coins": 1}})


def checkIfExists(discordUserId, discordUsername):

	discordUserId = int(discordUserId)
	exists = False
	results = coinsCluster.find({"_id": discordUserId})
    
	for result in results:
		try:
			if result["coins"] is int:
				try:
					if result["username"] is str:
						try:
							if result["minecraft"] is str:
								exists = True
						except KeyError:
							coinsCluster.update_one({"_id": discordUserId}, {"minecraft": "None"})
				except KeyError:
					coinsCluster.update_one({"_id": discordUserId, "username": discordUsername})
		except KeyError:
			coinsCluster.update_one({"_id": discordUserId}, {"coins": 1})
	if not exists:
		try:
			coinsCluster.insert_one({"_id": discordUserId, "username": discordUsername, "coins": 1, "minecraft": "None"})
		except pymongo.errors.DuplicateKeyError:
			pass
    


def removeCoins(userID, coinsToRemove):

    coins = coinsCluster.find({"_id": userID})
    data = 0

    for result in coins:
        data = result["coins"]
    
    if data < coinsToRemove:
        return False

    elif data >= coinsToRemove:
        coinsToRemove -= coinsToRemove * 2
        coinsCluster.update_one({"_id": userID}, {"$inc": {"coins": coinsToRemove}})
        return True


def getallcoins() -> list:
    coinlist = []
    data = coinsCluster.find({})
    for result in data:
        coinlist.append({"userid": result["_id"], "coins": result["coins"]})
    return coinlist


def getallusernames() -> list:
    coinlist = []
    data = coinsCluster.find({})
    for result in data:
        coinlist.append({"userid": result["_id"], "username": result["username"]})
    return coinlist


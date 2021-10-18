import json
import firebase_admin
import google.api_core.exceptions as googleException
from firebase_admin import credentials
from firebase_admin import firestore


firestoreCredentials = credentials.Certificate("firestore-credentials.json")
firebase_admin.initialize_app(firestoreCredentials)

firestoreDB = firestore.client()
coinsConnectionPath = firestoreDB.collection("coins")


def addCoins(userID):
    userID = str(userID)
    
    try:
        coinsPath = coinsConnectionPath.document(userID)
        coinsPath.update({"userid": userID})

        try:
            totalcoins = coinsPath.get().to_dict()["coins"]
            coinsPath.update({"coins": totalcoins + 1})
        except KeyError:
            coinsPath.update({"coins": 1})
    except googleException.NotFound:
        coinsPath = coinsConnectionPath.document(userID).create({})


def checkIfExists(discordUserId):

    try:
        coinsPath = coinsConnectionPath.document(discordUserId)
        coinsPath.update({"userid": discordUserId})
        try:
            coinsPath.update({"userid": discordUserId})
            coinsPath.get().to_dict()["coins"]

        except KeyError:
            coinsPath.update({"userid": discordUserId})
            coinsPath.update({"coins": 1})

    except googleException.NotFound:
        coinsConnectionPath.document(discordUserId).create({
            "userid": discordUserId, 
            "coins": 1
        })

def removeCoins(userID, coinsToRemove):
    
	userID = str(userID)

	coinsPath = coinsConnectionPath.document(userID)
	coinsPath.update({"userid": userID})
    
	checkIfExists(userID)

	coins = coinsPath.get().to_dict()["coins"]
    
	if coins < coinsToRemove:
		return False

	elif coins >= coinsToRemove:
		coinsPath.update({"coins": coins - coinsToRemove})
		return True


def getallcoins() -> list:
    coinsList = []
    for userData in coinsConnectionPath.get():
        coinsList.append(userData.to_dict())
    return coinsList

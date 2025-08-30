from pymongo import MongoClient

DB_NAME="AI-model"
# Connect to your local MongoDB server
client = MongoClient("mongodb://localhost:27017")

# Select your existing database
db = client[DB_NAME]

# List all collections inside the "suryansh" database
print("Collections:", db.list_collection_names())

# Select one specific collection (replace with your actual name)


def getCollection(name):
    return db[name]

def getCollectionList():
    return db.list_collection_names()

from pymongo import MongoClient
import os 

DB_NAME="AI-model"

mongo_uri=os.getenv("MONGO_URI","mongodb://localhost:27017")
# Connect to your local MongoDB server
client = MongoClient(mongo_uri)

# Select your existing database
db = client[DB_NAME]

# List all collections inside the "suryansh" database
print("Collections:", db.list_collection_names())

# Select one specific collection (replace with your actual name)


def getCollection(name):
    return db[name]

def getCollectionList():
    return db.list_collection_names()

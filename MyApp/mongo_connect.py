from pymongo import MongoClient

# Connect to your local MongoDB server
client = MongoClient("mongodb://localhost:27017")

# Select your existing database
db = client["AI-model"]

# List all collections inside the "suryansh" database
print("Collections:", db.list_collection_names())

# Select one specific collection (replace with your actual name)


def getCollection(name):
    return db[name]

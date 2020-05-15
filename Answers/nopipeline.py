import pymongo
from pymongo import MongoClient
uri = "mongodb+srv://bbcs:amazingrace@cluster0-d9jjq.mongodb.net/test?retryWrites=true&w=majority"
cluster = MongoClient(uri)

db = cluster.get_database("suspects_database")
collection = db.get_collection("suspects_collection")
#below is an alternative way of accessing our collection from cluster using square brackets
#db = cluster["suspects_database"]
#collection = db["suspects_collection"]

result1 = collection.count_documents({"$or": [
    {"registered": {"$regex": "^2017"}},
    {"registered": {"$regex": "^2018"}},
    {"registered": {"$regex": "^2019"}},
]})
print(result1)

result2 = collection.count_documents({
    "company": {"$regex": "^.E"}
})
print(result2)

result3 = collection.count_documents({
    "_id": {"$regex": "^5eb56f6e"}
})
print(result3)
# answer is 3213b5

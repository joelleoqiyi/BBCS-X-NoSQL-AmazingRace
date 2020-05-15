import pymongo
from pymongo import MongoClient
uri = "mongodb+srv://bbcs:amazingrace@cluster0-d9jjq.mongodb.net/test?retryWrites=true&w=majority"
cluster = MongoClient(uri)

db = cluster.get_database("suspects_database")
collection = db.get_collection("suspects_collection")
#below is an alternative way of accessing our collection from cluster using square brackets
#db = cluster["suspects_database"]
#collection = db["suspects_collection"]

pipeline = [
    {"$match": {"$or": [
        {"registered": {"$regex": "^2017"}},
        {"registered": {"$regex": "^2018"}},
        {"registered": {"$regex": "^2019"}},
    ]}}, #registered in 2018
    {"$count": "name"}
]

#returns you a cursor object so need to iterate through result to get the actual values.
result = collection.aggregate(pipeline)
for i in result:
    print (i)

pipeline1 = [
    {"$match":
        {"company": {"$regex": "^[A-Z]E"}}
    },
    {"$count": "company"}
]
#returns you a cursor object so need to iterate through result to get the actual values.
result1 = collection.aggregate(pipeline1)
for i in result1:
    print (i)


pipeline2 = [
    {"$match":
        {"_id": {"$regex": "^5eb56"}}
    },
    {"$count": "name"} #count the number of names, as each document is attached to a person with a name :) 
]
#returns you a cursor object so need to iterate through result to get the actual values.
result2 = collection.aggregate(pipeline2)
for i in result2:
    print (i)


# answer is 3213b5

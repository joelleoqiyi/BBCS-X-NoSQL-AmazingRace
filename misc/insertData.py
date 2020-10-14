# Add in URI statement before running this file to add the data to your MongoDB database. 

import pymongo
import json
from pymongo import MongoClient
uri = "insert_uri_here" # insert your URI statement here, make sure to allow write permissions for your mongodb user.
cluster = MongoClient(uri)

db = cluster.get_database("suspects_database")
collection = db.get_collection("suspects_collection")

# inserting into collection.
with open('data.json') as data_file:
  suspect_data = json.load(data_file)
  collection.insert_many(suspect_data)
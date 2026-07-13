from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["alt_credit_db"]
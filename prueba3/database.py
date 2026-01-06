from pymongo import MongoClient

def get_database():
    client = MongoClient("mongodb+srv://Steven:Steven2001@cluster0.mp8muds.mongodb.net/?appName=Cluster0")
    return client["Music"]
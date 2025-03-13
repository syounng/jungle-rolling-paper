from pymongo import MongoClient

#client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://test:test@13.236.160.185:27017/jungle9?authSource=admin&retryWrites=true&w=majority')
#client = MongoClient('mongodb://test:test@13.236.160.185:27017/?authMechanism=DEFAULT')
client = MongoClient('mongodb://test:test@13.236.160.185:27017/admin')



db = client.jungle9

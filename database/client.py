from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://jw142:gp1huwFEuma8pIlS@cluster0.dew2egn.mongodb.net"
client = MongoClient(uri, server_api=ServerApi('1'))


def getClient():
    return (client)







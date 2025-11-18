from pymongo import MongoClient
from json import load


def get_database():
    CONNECTION_STRING = "localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['labwork3']


def load_data(filename="data.json"):
    with open(filename) as inFile:
        result = load(inFile)
    return result


if __name__ == "__main__":
    labwork3 = get_database()
    leaders = labwork3["leaders"]
    data = load_data()
    leaders.insert_many(data)
    labwork3.client.close()
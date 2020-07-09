import json
import sys
import pymongo
import os
sys.path.append(".")
from data_feeder.data_adapter import DataAdapter
from urllib.parse import quote_plus


class MongoAdapter(DataAdapter):



    def __init__(self, host, port, db_name, user=None, password=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password

    def setup(self):
        params = {
            "username": quote_plus(self.user) if self.user else None,
            "password": quote_plus(self.password) if self.password else None,
            "host": self.host,
            "port": self.port,
        }
        if self.user and self.password:
            uri = "mongodb://{username}:{password}@{host}:{port}".format(**params)
        elif self.user:
            uri = "mongodb://{username}@{host}:{port}".format(**params)
        else:
            uri = "mongodb://{host}:{port}".format(**params)
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[self.db_name]
        try:
            print(self.client.server_info())
        except pymongo.errors.PyMongoError as exc:
            # import ipdb; ipdb.set_trace()
            print("Connection Error:", exc)
            print("Host: {host}, Port: {port}, Username: *** , Password: ***".format(**params))

    def clean(self):
        self.client.drop_database(self.db_name)

    def feed(self, collection_names, folder_name):



        arr = os.listdir()
        file_path = "../json_files/instances_val.json"
        with open(file_path, "r", encoding='utf-8') as f:
            json_data = json.load(f)

        for collection in collection_names:
            collection = self.db[collection]
            data = json_data[collection]
            for keys in data:
                keys["_id"] = keys["id"]
                del keys["id"]
                collection.insert_one(keys)

    # def duplicate_handling(self, set_of_ids, new_data, db, collection_name):
    #     for record in new_data:
    #         new_record = str(record["field_id"]) + str(record["image_id"])
    #         if new_record in set_of_ids:
    #             print(record + "is a duplicated record")
    #         else:
    #             collection = db[collection_name]
    #             collection.insert_one(record)



x = MongoAdapter("localhost", "27017", "test_db2", "blah", "blabla")
y = ["test1", "test2"]
x.setup(y)
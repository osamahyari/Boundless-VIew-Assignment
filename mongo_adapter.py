import json
import pymongo
from .data_adapter import DataAdapter


class MongoAdapter(DataAdapter):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["boundlessview"]
    list_of_collection_names = ["languages", "text_types", "fields", "categories", "tags", "images"]
    file_path = "../json_files/instances_val.json"
    with open(file_path, "r", encoding='utf-8') as f:
        json_data = json.load(f)

    def setup(self, db, db_name, list_of_collection_names):
        for collection_name in list_of_collection_names:
            db[collection_name]

    def clean(self, client, db_name):
        client.drop_database(db_name)

    def feed(self, db, collection_name, json_data):
        collection = db[collection_name]
        data = json_data[collection_name]
        collection.insert_many(data)

    def duplicate_handling(self, set_of_ids, new_data, db, collection_name):
        for record in new_data:
            new_record = str(record["field_id"]) + str(record["image_id"])
            if new_record in set_of_ids:
                print(record + "is a duplicated record")
            else:
                collection = db[collection_name]
                collection.insert_one(record)
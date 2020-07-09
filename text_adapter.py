import json
from src.data_adapters.data_adapter import DataAdapter


class TextAdapter(DataAdapter):

    list_of_collection_names = ["languages", "text_types", "fields", "categories", "tags", "images"]
    file_path = "../json_files/instances_val.json"
    with open(file_path, "r", encoding='utf-8') as f:
        json_data = json.load(f)

    def setup(self, collection_names, data):
        for col in collection_names:
            print(col + "Collection has been created\n")

    def clean(self, dbname):
        print(dbname + "Database has been deleted\n")

    def feed(self, collection_names, json_data):
        for col in collection_names:
            data = json_data[col]
            for dicts in data:
                ()
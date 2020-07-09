import pymongo
import json
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["boundlessview"]
collections = ["languages", "fields", "categories", "tags", "images"]
file_path = "../json_files/instances_val.json"
with open(file_path, "r", encoding='utf-8') as f:
    json_data = json.load(f)


def delete_all_collections(collection_list):
    for col in collection_list:
        collection = db[col]
        collection.drop()


def create_collections(collection_list):
    for col in collection_list:
        db[col]


def data_insertion(collection_list):
    for col in collection_list:
        data = json_data[col]
        collection = db[col]
        for keys in data:
            keys["_id"] = keys["id"]
            del keys["id"]
            collection.insert_one(keys)

        # collection.insert_many(data)


def reference_annotation_field():
    annotations = json_data["annotations"]
    for ann in annotations:
        ann["field"] = pymongo.database.DBRef(collection="fields", id=ann.pop("field_id"))
        ann["image"] = pymongo.database.DBRef(collection="images", id=ann.pop("image_id"))
        ann["_id"] = ann["id"]
        del ann["id"]
    collection = db["annotations"]
    collection.insert_many(annotations)


def duplicate_handling():
    annotations = json_data["annotations"]
    set_of_ids = set()
    for ann in annotations:
        field_image_ids = str(ann["field_id"]) + str(ann["image_id"])
        set_of_ids.add(field_image_ids)
        new_data = json_data["annotations"]
    for record in new_data:
        new_record = str(record["field_id"]) + str(record["image_id"])
        if new_record in set_of_ids:
            print(record, "is a duplicated record")
        else:
            collection = db["annotations"]
            collection.insert_one(record)
    collection = db["ann_ids"]






# delete_all_collections(collections)
# create_collections(collections)
# data_insertion(collections)
# duplicate_handling()
reference_annotation_field()



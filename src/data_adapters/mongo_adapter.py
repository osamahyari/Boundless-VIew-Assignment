from urllib.parse import quote_plus

import pymongo

from data_adapters.base_adapter import BaseAdapter


class MongoAdapter(BaseAdapter):

    def __init__(self, host, port, db_name, user=None, password=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password

        self.params = {
            "username": quote_plus(self.user) if self.user else None,
            "password": quote_plus(self.password) if self.password else None,
            "host": self.host,
            "port": self.port,
        }
        if self.user and self.password:
            uri = "mongodb://{username}:{password}@{host}:{port}".format(**self.params)
        elif self.user:
            uri = "mongodb://{username}@{host}:{port}".format(**self.params)
        else:
            uri = "mongodb://{host}:{port}".format(**self.params)
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[self.db_name]

    def setup(self):
        try:
            self.client.server_info()
            self.db["annotations"].create_index([("image_id", 1)])
            return True
        except pymongo.errors.PyMongoError as exc:
            print("Error Connecting:", exc)
            print("Host: {host}, Port: {port}, Username: *** , Password: ***".format(**self.params))
            return False

    def clean(self):
        self.client.drop_database(self.db_name)
        return "DB %s dropped" % self.db_name

    def feed_images(self, data, id_prefix):
        collection = self.db["images"]
        inserted_ids = []
        for image in data:
            image["_id"] = '%s_%s' % (id_prefix, image.pop("id"))
            try:
                # by default, insert implements retry
                inserted_ids.append(collection.insert(image))
            except pymongo.errors.DuplicateKeyError:
                print("Duplicate image:", image)
        return inserted_ids

    def feed_annotations(self, data, id_prefix):
        collection = self.db["annotations"]
        for ann in data:
            ann["field"] = pymongo.database.DBRef(collection="fields", id=ann["field_id"])
            ann["image"] = pymongo.database.DBRef(collection="images", id='%s_%s' % (id_prefix, ann["image_id"]))
            ann["tag"] = pymongo.database.DBRef(collection="tags", id=ann["tag_id"])
            ann["category"] = pymongo.database.DBRef(collection="categories", id=ann["category_id"])
            ann["_id"] = '%s_%s' % (id_prefix, ann.pop("id"))
        # by default, insert_many implements retry
        result = collection.insert_many(data)
        return result.inserted_ids

    def feed_meta(self, data):
        collection_names = ["languages", "fields", "categories", "tags"]
        final_result = {}
        for collection_name in collection_names:
            final_result[collection_name] = []
            collection = self.db[collection_name]
            for item in data[collection_name]:
                item["_id"] = item.pop("id")
                try:
                    final_result[collection_name].append(collection.insert(item))
                except pymongo.errors.DuplicateKeyError:
                    print("Duplicate", collection_name, ":", item)

        return final_result

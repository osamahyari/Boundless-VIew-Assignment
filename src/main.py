import json
import os
import sys

from data_adapters.data_adapter_factory import create_data_adapter


class DataFeeder(object):

    def __init__(self):
        self.collections = ["languages", "fields", "categories", "tags", "images"]

    def process(self, kwargs):
        data_files = self.get_files(args["data_folder"])
        adapter = create_data_adapter(**args)

        cleandb = kwargs["cleandb"]
        if cleandb:
            print("Cleaning DB...")
            print(adapter.clean())

        for index, data_file in enumerate(data_files):
            print("="*30)
            print("Processing", data_file)
            # import ipdb; ipdb.set_trace()
            with open(data_file, "r", encoding='utf-8') as f:
                data = json.load(f)
                self.process_data(data, adapter, index, **kwargs)

    def process_data(self, data, adapter, index, *args, **kwargs):
        if adapter.setup():
            print("Connection to DB setup successfully")
        else:
            print("Connection failed. Exiting")
            exit(0)

        annotations = data["annotations"]
        print("-"*10, "Detecting Duplicate Annotations", "-"*10)
        msg, duplicates = self.detect_duplicate_annotations(annotations)
        print(msg)
        annotations = self.remove_duplicates(annotations, duplicates)

        images = data["images"]
        print("-"*10, "Detecting Duplicate Images", "-"*10)
        msg, duplicates = self.detect_duplicate_images(images)
        print(msg)
        images = self.remove_duplicates(images, duplicates)

        print("\nInserting Meta Collections")
        result = adapter.feed_meta(data)

        for col_name, ids in result.items():
            print("Inserted", len(ids), col_name, ":", ids)

        result = adapter.feed_images(images, index)
        print("\nInserted", len(result), "images.", result)

        result = adapter.feed_annotations(annotations, index)
        print("\nInserted", len(result), "annotations.")

    def remove_duplicates(self, collection, duplicates):
        items_by_id = {
            item["id"]: item
            for item in collection
        }
        for dup in duplicates:
            for i in range(1, len(dup)):
                del items_by_id[dup[i]]
        return items_by_id.values()

    def detect_duplicate_annotations(self, annotations):
        hashes = {}
        msg = "Found Duplicate Annotations: "

        for ann in annotations:
            hash = self.hash_annotation(ann)
            hashes[hash] = hashes.get(hash, [])
            hashes[hash].append(ann["id"])

        found_duplicates = False
        duplicates = []
        for hash, annotation_ids in hashes.items():
            if len(annotation_ids) > 1:
                found_duplicates = True
                msg += "\nAnnotation ids: %s" % (','.join(map(str, annotation_ids)))
                duplicates.append(annotation_ids)

        if not found_duplicates:
            msg += "0"
        return msg, duplicates

    def detect_duplicate_images(self, images):
        file_names = {}
        msg = "Found Duplicate Images: "

        for img in images:
            file_names[img["file_name"]] = file_names.get(img["file_name"], [])
            file_names[img["file_name"]].append(img["id"])

        duplicates = []
        found_duplicates = False
        for file_name, image_ids in file_names.items():
            if len(image_ids) > 1:
                found_duplicates = True
                msg += "\nImage ids: %s" % (','.join(map(str, image_ids)))
                duplicates.append(image_ids)
        if not found_duplicates:
            msg += "0"
        return msg, duplicates

    def hash_annotation(self, annotation):
        return str(annotation["field_id"])+str(annotation["image_id"])

    def get_files(self, data_folder):
        """
        Return a list of file paths which exist inside the data folder
        """
        data_folder_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', data_folder
        ))
        data_files = [
            os.path.join(data_folder_path, f)
            for f in os.listdir(data_folder_path)
            if os.path.isfile(os.path.join(data_folder_path, f))
        ]
        return data_files


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Incorrect parameters, received:", sys.argv[1:])
        print("Expected parameters: dry_run, host, port, username, password,"
              "dbname, cleandb, data_folder")
        exit(0)

    _, dry_run, host, port, username, password, dbname, cleandb, data_folder = sys.argv
    if username == "unset" or password == "unset":
        username = None
        password = None

    dry_run = int(dry_run)
    cleandb = int(cleandb)

    args = {
        "dry_run": dry_run,
        "host": host,
        "port": port,
        "username": "***",
        "password": "***",
        "dbname": dbname,
        "cleandb": cleandb,
        "data_folder": data_folder,
    }

    print("Received arguments (masking username and password): ", args)

    args["username"] = username
    args["password"] = password

    DataFeeder().process(args)

    print("Completed precessing the data. Thank you, come again :-) ... Osama Alhyari")

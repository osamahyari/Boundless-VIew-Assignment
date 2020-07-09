from data_adapters.text_adapter import TextAdapter
from data_adapters.mongo_adapter import MongoAdapter


def create_data_adapter(dry_run, host, port, username, password, dbname):
    if dry_run:
        return TextAdapter()
    else:
        return MongoAdapter(host, port, dbname, username, password)

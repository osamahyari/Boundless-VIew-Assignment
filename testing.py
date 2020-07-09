from .data_adapter import DataAdapter
from .mongo_adapter import MongoAdapter
import pymongo
from urllib.parse import quote_plus

x = MongoAdapter("localhost", "27017", "test_db")
y = ["test1", "test2"]
x.setup(y)
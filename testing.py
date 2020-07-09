from src.data_adapters.mongo_adapter import MongoAdapter

x = MongoAdapter("localhost", "27017", "test_db")
y = ["test1", "test2"]
x.setup(y)
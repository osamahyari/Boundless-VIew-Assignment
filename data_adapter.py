from abc import ABC



class DataAdapter(ABC):

    def __init__(self):
        pass

    def setup(self, db_name):
        pass

    def clean(self, db_name):
        pass

    def feed(self, data, collection_name):
        pass

    def duplicate_handling(self):
        pass






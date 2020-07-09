from data_adapters.base_adapter import BaseAdapter


class TextAdapter(BaseAdapter):

    def setup(self):
        raise NotImplementedError

    def clean(self):
        raise NotImplementedError

    def feed_images(self, data):
        raise NotImplementedError

    def feed_annotations(self, data):
        raise NotImplementedError

    def feed_meta(self, data):
        raise NotImplementedError

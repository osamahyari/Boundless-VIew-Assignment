import abc


class BaseAdapter(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def clean(self):
        pass

    @abc.abstractmethod
    def feed_images(self, data):
        pass

    @abc.abstractmethod
    def feed_annotations(self, data):
        pass

    @abc.abstractmethod
    def feed_meta(self, data):
        pass

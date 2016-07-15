

class Config(object):
    """ Configuration object, holds information about Elasticsearch. """
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self):
        self.__url = None
        self.__index = None
        self.__username = None
        self.__password = None
        self.__full_link = None

        self.__host = None
        self.__port = None

        self.__auth = None

        self.analysis_doc_type = None
        self.request_doc_type = None

        self.index_name = None

    def initialize(self, config):
        pass

    def get_index(self):
        return self.index_name

    def get_analysis_doc_type(self):
        return self.analysis_doc_type

    def get_request_doc_type(self):
        return self.request_doc_type

    def search_url(self):
        return self.__full_link

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def auth(self):
        return self.__auth

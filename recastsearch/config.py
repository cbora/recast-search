import os

class Config(object):
    """ Configuration object, holds information about Elasticsearch. """
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self):
        self.__host = os.environ.get('RECASTSEARCH_HOST', 'localhost')
        self.__port = os.environ.get('RECASTSEARCH_PORT', 443)
        self.__auth = os.environ.get('RECASTSEARCH_PORT', None)
        self.__use_ssl = os.environ.get('RECASTSEARCH_USESSL', True)
        self.__index = os.environ.get('RECASTSEARCH_INDEX', 'recast')
        self.__analysis_doc_type = os.environ.get('RECASTSEARCH_ANALYSIS', 'analysis')
        self.__request_doc_type = os.environ.get('RECASTSEARCH_REQUEST', 'request')

        self.__url = 'http://{}{}:{}'.format(self.__auth, self.__host, self.__port)

    def initialize(self, config):
        pass

    def get_index(self):
        return self.index_name

    def get_analysis_doc_type(self):
        return self.analysis_doc_type

    def get_request_doc_type(self):
        return self.request_doc_type

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def auth(self):
        return self.__auth

    def url(self):
        return self.__url

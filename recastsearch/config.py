import os
import yaml

class Config(object):
    """ Configuration object, holds information about Elasticsearch. """
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, config_file=None):
        if config_file:
            f = open(config_file)
            config = yaml.load(f)
            f.close()

            os.environ['RECASTSEARCH_HOST'] = config.get('HOST', '')
            os.environ['RECASTSEARCH_PORT'] = config.get('PORT', '443')
            os.environ['RECASTSEARCH_AUTH'] = config.get('AUTH', '')
            os.environ['RECASTSEARCH_USE_SSL'] = config.get('USE_SSL', 'True')
            os.environ['RECASTSEARCH_INDEX'] = config.get('INDEX', 'recast')
            os.environ['RECASTSEARCH_ANALYSIS'] = config.get('ANALYSIS', 'analysis')
            os.environ['RECASTSEARCH_REQUEST'] = config.get('REQUEST', 'request')
            
        self.__host = os.environ.get('RECASTSEARCH_HOST', 'localhost')
        self.__port = os.environ.get('RECASTSEARCH_PORT', 443)
        self.__auth = os.environ.get('RECASTSEARCH_AUTH', '')
        self.__use_ssl = os.environ.get('RECASTSEARCH_USESSL', 'True')
        self.__index = os.environ.get('RECASTSEARCH_INDEX', 'recast')
        self.__analysis_doc_type = os.environ.get('RECASTSEARCH_ANALYSIS', 'analysis')
        self.__request_doc_type = os.environ.get('RECASTSEARCH_REQUEST', 'request')

        self.__url = 'https://{}@{}'.format(self.__auth, self.__host)

        response = os.system("ping -c 1 " + self.__url)
        if response:
            print self.__url, ' is up!'
        else:
            print self.__url, ' is down!'

    def initialize(self, config):
        pass

    def index(self):
        return self.__index

    def analysis_doc_type(self):
        return self.__analysis_doc_type

    def request_doc_type(self):
        return self.__request_doc_type

    def host(self):
        return self.__host

    def port(self):
        return int(self.__port)

    def auth(self):
        return self.__auth

    def url(self):
        return self.__url

    def use_ssl(self):
        if self.__use_ssl == 'True':
            return True
        else:
            return False

    def __repr__(self):
        return "<Config(url: %r)>" % self.__url

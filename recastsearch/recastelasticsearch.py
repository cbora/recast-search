from elasticsearch import Elasticsearch
#from pyelasticsearch.exceptions import IndexAlreadyExistsError
from config import Config

class RecastElasticSearch(object):
    """ High level elasticsearch API for Recast. """
    
    def __init__(self, config):

        self.config = config
        self.es = Elasticsearch([{'host': self.config.host(),
                                  'port': self.config.port(),
                                  'use_ssl': self.config.use_ssl(),
                                  'http_auth': self.config.auth()
                                  }])

    def create(self):
        """ creates index. """
        # ignore index already exists error
        self.es.indices.create(index=self.config.index(), ignore=400)

    def delete(self):
        """ (careful) deletes index and everything contained. """
        self.es.indices.delete(index=self.config.index(), ignore=[400, 404])

    def query_builder(self, query):
        """ builds query body for search. """
        body = {
            'query': {
                'filtered': {
                    'query': {
                        'query_string': {
                            'query': query
                            }
                        }
                    }
                }
            }
        return body

    def pretty_response(self, response):
        """ Cleans response, removes unrelevant info. """
        if response.has_key('hits'):
            if response['hits'].has_key('hits'):
                return response['hits']['hits']

        raise Exception('Unconventional response!')

    def isEmpty(self, doc_type):
        """ checks if elastic search is empty.
        
        :returns True if empty otherwise false.
        """
        if not doc_type:
            raise Exception('No doc_type provided!')
        if doc_type == self.config.analysis_doc_type():
            return not bool(self.all_analyses())
        if doc_type == self.config.request_doc_type():
            return not bool(self.all_requests())

    def all_analyses(self):
        """ returns all analyses. """
        response = self.es.search(index=self.config.index(),
                                  doc_type=self.config.analysis_doc_type(),
                                  body={"query": {"match_all": {}}})
        return self.pretty_response(response)

    def all_requests(self):
        """ returns all requests. """
        response = self.es.search(index=self.config.index(),
                                  doc_type=self.config.request_doc_type(),
                                  body={"query": {"match_all": {}}})
        return self.pretty_response(response)

    def advanced_search(self, doc_type, body):
        """ Perform advanced search, user provides search body. """
        response = self.es.search(index=self.config.index(),
                                  doc_type=doc_type,
                                  body=body)
        return self.pretty_response(response)
                                                 
    def simple_search(self, query, doc_type):
        """ simple search. 
        
        :returns list containing 
        """
        if not query:
            raise Exception('Empty query!')
        if not doc_type:
            raise Exception('No doc type provided!')
        
        body = self.query_builder(query=None)
        response = self.es.search(index=self.config.index(),
                                  doc_type=doc_type,
                                  body=body)
        return self.pretty_response(response)
                                      
    def search_analysis(self, query):
        """ Search for analysis.

        :param query: search keywords or string
        :Returns JSON object containing ranked results.
        """
        body = self.query_builder(query=query)
        print self.config.index()
        print self.config.analysis_doc_type()
        print body
        response = self.es.search(index=self.config.index(),
                                  doc_type=self.config.analysis_doc_type(),
                                  body = body)

        return self.pretty_response(response)

    def search_request(self, query):
        """ Search for requests.
        
        :param query: search keywords or string
        :Returns JSON object contained ranked results.
        """
        body = self.query_builder(query=query)
        response = self.es.search(index=self.config.index(),
                                  doc_type=self.config.request_doc_type(),
                                  body=body)
        return self.pretty_response(response)

    def add_analysis(self, content):
        """ Adds single analysis content to ES. 

        """
        self.es.index(self.config.index(), self.config.analysis_doc_type(), content)

    def add_request(self, content):
        """ Adds single request content to ES.

        """
        self.es.index(self.config.index(), self.config.request_doc_type(), content)

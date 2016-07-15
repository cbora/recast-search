from pyelasticsearch import ElasticSearch
from pyelasticsearch.exceptions import IndexAlreadyExistsError

class RecastElasticSearch(object):
    """ High level elasticsearch API for Recast. """
    
    def __init__(self, config):

        self.config = config
        self.es = Elasticsearch([{'host': self.config.host_name(),
                                  'port': self.config.port(),
                                  'use_ssl': self.config.use_ssll(),
                                  'http_auth': self.config.auth()
                                  }])

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
    
    def isEmpty(self, doc_type):
        """ checks if elastic search is empty.
        
        :returns True if empty otherwise false.
        """
        if not doc_type:
            raise Exception('No doc_type provided!')
        
        return not bool(self.analyses)

    def analyses(self):
        """ returns all analyses. """
        body = self.query_builder(query=None)
        response = self.es.search(index=self.config.index(),
                                  doc_type=doc_type,
                                  body=body)
        return response

    def requests(self):
        """ returns all requests. """
        body = self.query_builder(query=None)
        response = self.es.search(index=self.config.index(),
                                  doc_type=doc_type,
                                  body=body)
        return response
                                                 
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
        return response
                                      
    def search_analysis(self, query):
        """ Search for analysis.

        :param query: search keywords or string
        :Returns JSON object containing ranked results.
        """
        body = self.query_builder(query=query)
        response = self.es.search(index=self.config.index(),
                                  doc_type=self.config.analysis_type,
                                  body = body)

        return response

    def search_request(self, query):
        """ Search for requests.
        
        :param query: search keywords or string
        :Returns JSON object contained ranked results.
        """
        body = self.query_builder(query=query)
        response = self.es.search(index=self.config.index(),
                                  doc_type=self.config.request_type,
                                  body=body)
        return response


    def add_analysis(self, content):
        """ Adds single analysis content to ES. 

        """
        self.es.index(self.config.index(), config.analysis_type(), content)

    def add_request(self, content):
        """ Adds single request content to ES.

        """
        self.es.index(self.config.index(), config.request_type(), content)

        
            
            

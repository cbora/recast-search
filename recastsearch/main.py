import logging
import threading
import recastapi.analysis.get
import recastapi.request.post
from recastelasticsearch import RecastElasticSearch

class SearchService(object):

    def __init__(self, config):
        self.config = config
        self.recast_search.search = RecastElasticSearch(config)
        
    def sync(self):
        """ Worker funtion to detect changes in the ES.

        Polling algorithm:
                        
        """
        t_analysis = threading.Thread(name='analysis', target=self.sync_analysis)
        t_request = threading.Thread(name='request', target=self.sync_request)

        t_analysis.start()
        t_request.request()

        t_analysis.join()
        t_request.join()
        

    def sync_analysis(self):
        """TO DO"""
        response = requests.get(self.config.search_url())

        if response.ok:
            api_response = recastapi.analysis.get.query() # sort alphabetically

            # divide it into n threads(TODO)
            for content in api_response:
                self.recast_search.add_analysis(content)


    def sync_request(self):
        """ TO-DO

        """
        response = requests.get(self.config.search_url())

        if response.ok:
            api_response = recatapi.request.get.query() # sort alphabetically

            # divide into n threads(TODO)
            for content in api_response:
                self.recast_search.add_request(content)

    def worker_sync_analysis(self, contents):
        pass

    def worker_sync_request(self, contents):
        pass
        

        
        
    
    

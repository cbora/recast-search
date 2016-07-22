import logging
from operator import itemgetter
import Queue
import recastapi.analysis.get
import recastapi.request.get
from recastelasticsearch import RecastElasticSearch
import threading


class SyncService(object):
    """ Service to sync ES instance and frontend database. """
    def __init__(self, config):
        self.config = config
        self.recast_search = RecastElasticSearch(config)
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(levelname)s] %(message)s')
        
    def sync(self):
        """ Worker funtion to detect changes in the ES.
        algorithm diffs two sorted Queues from ES and DB,
              adds or deletes records from ES accordingly.
        """
        t_analysis = threading.Thread(name='analysis', target=self.sync_analysis)
        t_request = threading.Thread(name='request', target=self.sync_request)
        logging.info('Start Analysis sync')
        t_analysis.start()
        logging.info('Start Request sync')
        t_request.request()

        t_analysis.join()
        t_request.join()
        

    def sync_analysis(self):
        """ Function to sync analyses in the DB and ES. """
        api_responses = recastapi.analysis.get.analysis()
        # if es is empty, do a bulk insert(optimized)
        if self.recast_search.isEmpty(doc_type=self.config.analysis_doc_type()):
            self.recast_search.bulk_analyses(api_responses)
            return

        es_responses = self.recast_search.all_analyses()
        sorted_api_responses = sorted(api_responses, key=itemgetter('title'))
        sorted_es_responses = sorted(es_responses, key=lambda e: e['_source']['title'])

        api_queue = Queue.Queue()
        es_queue = Queue.Queue()
        for r in sorted_api_responses:
            api_queue.put(r)
        for r in sorted_es_responses:
            es_queue.put(r)

        while not es_queue.empty():
            es_tmp = es_queue.get()
            size = api_queue.qsize()
            i = 0
            match = False
            while i < size:
                i += 1
                api_tmp = api_queue.get()
                if es_tmp['_source']['title'] == api_tmp['title']:
                    match = True
                    break
                api_queue.put(api_tmp)
            if not match:
                # if an element didn't get a match we delete it
                # it is no longer in the DB
                self.recast_search.delete_record(self.config.analysis_doc_type(),
                                                 'id: {}'.format(es_tmp['id'])
                                                 )
        # Add the elements that didn't get a match to ES.
        while not api_queue.empty():
            self.recast_search.add_analysis(api_queue.get())
            
    def sync_request(self):
        """ Function to sync request in the DB and ElasticSearch.
        """
        api_responses = recastapi.request.get.request()
        if self.recast_search.isEmpty(doc_type=self.config.analysis_doc_type()):
            self.recast_search.bulk_requests(api_response)
            return
        es_responses = self.recast_search.all_requests()
        sorted_api_responses = sorted(api_responses, key=itemgetter('title'))
        sorted_es_responses = sorted(es_responses, key=lambda e: e['_source']['title'])

        api_queue = Queue.Queue()
        es_queue = Queue.Queue()
        for r in sorted_api_responses:
            api_queue.put(r)
        for r in sorted_es_responses:
            es_queue.put(r)

        while not es_queue.empty():
            es_tmp = es_queue.get()
            size = api_queue.qsize()
            i = 0
            match = False
            while i < size:
                i += 1
                r_tmp = api_queue.get()
                if es_tmp['_source']['title'] == r_tmp['title']:
                    match = True
                    break
                api_queue.put(r_tmp)
            if not match:
                # delete the no-match (no longer exists in DB)
                self.recast.delete_record(self.config.request_doc_type(),
                                          'id: {}'.format(es_tmp['id']))
        while not api_queue.empty():
            self.recast_search.add_request(api_queue.get())
        

        
        
    
    

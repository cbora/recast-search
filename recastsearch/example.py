from recastsearch.config import Config
from recastsearch.recastelasticsearch import RecastElasticSearch
from recastsearch.sync import SyncService

# Example usage of the search and sync services
# need to pass a text based configuration file to the Config class
# other classes will use this object to point to the ES instance.

config = Config('recastsearch/resources/default.yaml')

sync = SyncService(config)

# sync analysis and request(ideally these functions will go in an infinite loop)
sync.sync_analysis()

sync.sync_request()

# Do some search using recastES api
search = RecastElasticSearch(config)

search.search_analysis('ATLAS')

search.search_analysis('CMS')


# retrieve all analyses & requests

search.all_analyses()


search.all_requests()


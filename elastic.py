from elasticsearch import Elasticsearch
es = Elasticsearch()

# ignore 400 cause by IndexAlreadyExistsException when creating an index
es.indices.create(index='test-index', ignore=400)

es.search(index='test-index', filter_path=['hits.hits._id', 'hits.hits._type'])
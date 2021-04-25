import os

import pymongo
from cachetools.func import ttl_cache


@ttl_cache(ttl=900)
def mongo_client(environment_variable='MONGO_URI'):
    """Get a connection to mongodb via MONGO_URI env variable"""

    mongo_uri = os.environ.get(environment_variable)
    return pymongo.MongoClient(mongo_uri).get_database()



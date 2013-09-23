# Copyright 2013 Mitchell Stanton-Cook Licensed under the
# Educational Community License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
# http://www.osedu.org/licenses/ECL-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.

#import pymongo


def get_db(cfg, admin=False):
    """
    Return a mongodb defined in the config object or the admin DB
    """
    connection = pymongo.MongoClient('localhost', cfg['port'])
    if not admin:
        return connection[cfg['db']]
    else:
        return connection['admin']

def get_collection(cfg, collection_name):
    """
    Return a mongodb collection (like a table) given the name
    """
    db = get_db(cfg)
    coll = db[collection_name]
    # Make below into logger
    #print coll
    return coll

def get_db_stats(cfg):
    db = get_db(cfg)
    tmp = db.command("dbStats")
    print "Operating on %s DB with %i objects" % (tmp['db'], tmp['objects'])

def create_search_index(cfg, collection_name, element):
    """
    Enable text search on a collection element

    See: http://blog.mongodb.org/
            post/52139821470/integrating-mongodb-text-search-with-a-python-app
    """
    db = get_db(cfg, admin=True)
    db.command("setParameter", textSearchEnabled=True)
    db = get_db(cfg)
    db[collection_name].ensure_index([
          (element, 'text'),
      ],
      name="search_index",
    )

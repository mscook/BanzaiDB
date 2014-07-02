# Copyright 2013-2014 Mitchell Stanton-Cook Licensed under the
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

import re

import rethinkdb as r
from rethinkdb.errors import RqlDriverError

from BanzaiDB import config
from BanzaiDB import errors


def make_connection():
    """
    Make a connection to the RethinkDB database

    Pulls settings (host, port, database name & auth_key from
    BanzaiDBConfig())

    ..note:: The RethinkDB connection is a context manager. Thus use this
             funtion like 'with make_connection():'

    :returns: a connection context manager
    """
    cfg = config.BanzaiDBConfig()
    if not re.match("^[a-zA-Z0-9_]+$", cfg['db_name']):
        raise errors.InvalidDBName(cfg['db_name'])
    try:
        connection = r.connect(host=cfg['db_host'], port=cfg['port'],
                               db=cfg['db_name'], auth_key=cfg['auth_key'])
    except RqlDriverError:
        raise RqlDriverError("No database connection could be established.")
    return connection

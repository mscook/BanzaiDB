Initialising your first BanzaiDB database
=========================================

Initialising a BanzaiDB involves having BanzaiDB connect to your RethinkDB 
instance. Once connected BanzaiDB creates a database and initialises some 
default tables.

Prerequisites
-------------

Please ensure the following has been met:
    # You have installed BanzaiDB, RethinkDB & the RethinkDB python driver   
    # You have a RethinkDB instance running

Telling BanzaiDB about your RethinkDB instance
----------------------------------------------

The file ~/.BanzaiDB.cfg (~/ = /home/$USER/) is used to provide information to 
Banzai DB about your RethinkDB instance.

An example would be::

    db_host = 127.0.0.1
    db_name = my-cool-project

*db_host:* will always be 127.0.0.1 unless you have installed your RethinkDB
instance on a remote server.

*db_name:* will typically reflect the short running title of the project



BanzaiDB
========

BanzaiDB is a tool that:
    * puts the results of NGS experiments into a (NoSQL) datastore
    * provides a set of generalised query functions to wrangle with the data
      stored in the datastore.

**BanzaiDB is a generalised framework for pairing NGS analysis with 
the RethinkDB database.**

BanzaiDB is based on the Banzai NGS pipeline workflow and thus is geared 
towards handling data generated from Velvet (assembly), Nesoni (mapping/
variant calling), Mugsy (whole genome alignment) BRATTNextGen 
(recombination detection) and Prokka (annotation) tools.

*The present focus is storing SNPs and recombination analysis.*

**This is not a stable API.** 


Requirements
------------

You'll need a:
    * A RethinkDB server/instance (from http://www.rethinkdb.com/) running 
      locally

Python modules (these can be pip installed):
    * rethinkdb
    * biopython
    * reportlab
    * fabric
    * tablib

To increase the rethinkdb client performance performance::

    protoc --version
    wget http://protobuf.googlecode.com/files/protobuf-2.4.1.tar.gz
    tar -zxvf protobuf-2.4.1.tar.gz
    cd protobuf-2.4.1/
    cd python/
    python setup.py install
    export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp


Assumptions
-----------

**1)** You have a RethinkDB instance running, You can give information about 
this instance to BanzaiDB using::

    db_host = 152.99.100.101
    db_name = BLAH_RUN

In the file **~/.BanzaiDB.cfg**

**2)** You have downloaded and installed all required 3rd party python modules
and have successfully install BanzaiDB.

**3)** Write the rest...

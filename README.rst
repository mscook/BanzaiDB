.. image:: https://raw.github.com/mscook/BanzaiDB/master/misc/BanzaiDB.png
    :alt: BanzaiDB logo

|

.. image:: http://gitshields.com/v2/text/API/Unstable/red.png

|

.. image:: http://gitshields.com/v2/drone/github.com/mscook/BanzaiDB/brightgreen-red.png

|

.. image:: https://landscape.io/github/mscook/BanzaiDB/master/badges


What is BanzaiDB?
-----------------

BanzaiDB is a tool for pairing Microbial Genomics Next Generation Sequencing 
(NGS) analysis with a NoSQL_ database. We use the RethinkDB_ NoSQL database.

BanzaiDB:
    * initalises the NoSQL database and associated tables,
    * populates the database with results of NGS experiments/analysis and,
    * provides a set of query functions to wrangle with the data stored within 
      the database.


Why BanzaiDB?
-------------

Downstream analysis (secondary/tertiary) of large collections of draft 
microbial genomes typically generates many separate flat files. 

The bioinformatician will:
    * write scripts to parse and extract the important information from 
      the results files (often trying to standardise the output from 
      similar programs),
    * store these results in further flat files,
    * write scripts to link the results of one analysis step to another,
    * store these results in further flat files,
    * modify scripts as hypothesis is improved as a direct consequence of
      incorporating the knowledge from the previous steps,
    * ...
    * ...
    * ...
    * end up with thousands of flat files, many many scripts and generally get 
      confused as to how and where everything came from.

The idea around BanzaiDB is to run once, store once anlyse many times.


About BanzaiDB
--------------

BanzaiDB is geared towards outputs of Bioinformatics software employed by 
the `Banzai NGS pipeline`_. 

BanzaiDB is thus geared towards handling data generated from:
    * Velvet and SPAdes (assembly), 
    * BWA and Nesoni (mapping/variant calling),
    * Mugsy (whole genome alignment), 
    * BRATTNextGen (recombination detection) and,
    * Prokka (annotation).

*The present focus is on storing and manipulating the results of SNP and 
recombination analysis.*

**Banzai is not a stable API.** 

See the ReadTheDocs site for `BanzaiDB documentation`_ (User & API).


About RethinkDB
---------------

We choose RethinkDB_ as our underlying database for a few reasons:
    * RethinkDB is both developer and operations friendly. This sits well with 
      the typical bioinforatician,
    * NoSQL databases allow for a felxible schema. We can store/collect now, 
      think later. This is much like how science is performed.
    * Not every bioinformatician or lab has a system administrator. RethinkDB 
      is easy to setup and administer
    * We don't know how big our complex our datasets could get in the future. 
      It is easy to scale RethinkDB into a cluster.
    * ReQL the underlying query language is nice and simple to
      learn/understand. We're also very confortable with Python and the 
      availability of official python drivers (also javascript & ruby, and a 
      heap for user contributed for a swag of languages) is a big bonus.


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

    $ protoc --version
    $ wget http://protobuf.googlecode.com/files/protobuf-2.4.1.tar.gz
    $ tar -zxvf protobuf-2.4.1.tar.gz
    $ cd protobuf-2.4.1/
    $ cd python/
    $ python setup.py install
    $ export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp




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



Usage
-----

Something like this::

    $ python BanzaiDB.py -h
    usage: BanzaiDB.py [-h] [-v] {init,populate,update,query} ...

    BanzaiDB v0.1 - Database for Banzai NGS pipeline tool
    (http://github.com/mscook/BanzaiDB)

    positional arguments:
      {init,populate,update,query}
                            Available commands:
        init                Initialise a DB
        populate            Populates a database with results of an experiment
        update              Updates a database with results from a new experiment
        query               List available or provide database query functions

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         verbose output

    Licence: ECL 2.0 by Mitchell Stanton-Cook <m.stantoncook@gmail.com>




Default BanzaiDB table schema
-----------------------------

On intialisation the following database tables will be generated:
    * strains,
    * metadata
    * variants,
    * ref
    * ref_features

More information can be found in tables.rst


.. _RethinkDB: http://www.rethinkdb.com
.. _NoSQL: http://nosql-database.org
.. _Banzai NGS pipeline: https://github.com/mscook/Banzai-MicrobialGenomics-Pipeline
.. _BanzaiDB documentation: http://banzaidb.readthedocs.org


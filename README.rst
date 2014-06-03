.. image:: https://raw.github.com/mscook/BanzaiDB/master/misc/BanzaiDB.png
    :alt: BanzaiDB logo

----

.. image:: http://gitshields.com/v2/text/API/Unstable/red.png
   :alt: API stability

|

.. image:: https://landscape.io/github/mscook/BanzaiDB/master/landscape.png
   :target: https://landscape.io/github/mscook/BanzaiDB/master
   :alt: Code Health

|

.. image:: http://gitshields.com/v2/drone/github.com/mscook/BanzaiDB/brightgreen-red.png
   :target: https://drone.io/github.com/mscook/BanzaiDB
   :alt: Build status (Drone.io)


What is BanzaiDB?
-----------------

BanzaiDB is a tool for pairing Microbial Genomics Next Generation Sequencing 
(NGS) analysis with a NoSQL_ database. We use the RethinkDB_ NoSQL database.

BanzaiDB:
    * initialises the NoSQL database and associated tables,
    * populates the database with results of NGS experiments/analysis and,
    * provides a set of query functions to wrangle with the data stored within 
      the database.


Why BanzaiDB?
-------------

The analysis (primary/secondary/tertiary) of large collections of draft 
microbial genomes from NGS typically generates many separate flat files. 

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
    * end up with thousands of flat files, many scripts and generally get 
      confused as to how and where everything came from.

**The idea around BanzaiDB is to run once, store once analyse many times.**


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
      the typical bioinformatician,
    * NoSQL databases allow for a flexible schema. We can store/collect now, 
      think later. This is much like how science is performed.
    * Not every bioinformatician or lab has a system administrator. RethinkDB 
      is easy to setup and administer
    * We don't know how big our complex our datasets could get in the future. 
      It is easy to scale RethinkDB into a cluster.
    * ReQL the underlying query language is nice and simple to
      learn/understand. We're also very comfortable with Python and the 
      availability of official python drivers (also JavaScript & Ruby, and a 
      heap for user contributed for a swag of languages) is a big bonus.


BanzaiDB Requirements
---------------------

You will need:
    * (probably) administrator access to your machine(s)
    * a RethinkDB_ server/instance. This can be running locally or on a VPS, 
    * git (to clone this repository) and
    * pip_

You will also need a few Python modules:
    * rethinkdb
    * biopython
    * reportlab
    * fabric
    * tablib
    * argparse (if Python 2.6)

The Python modules should/will be pulled down automatically when installing 
BanzaiDB.

We recommend you increase the rethinkdb python `driver performance`_. We have 
found that in some cases the installation of C++ backend fails. `We provide`_ 
a simple protocol that we have found works.


BanzaiDB Installation
---------------------

Something like this::

    $ git clone https://github.com/mscook/BanzaiDB.git
    $ cd BanzaiDB
    $ python setup.py install


Getting BanzaiDB talking to RethinkDB
-------------------------------------

You provide information about you RethinkDB instance and database using the 
file **~/.BanzaiDB.cfg** (~/ is shorthand for $HOME).

The configuration file supports::

    db_host  =  [def = localhost]
    port     =  [def = 28015]
    db_name  =  [def = Banzai]
    auth_key =  [def = '']


BanzaiDB usage
--------------

**Note:** Please refer to the `BanzaiDB documentation`_ (via ReadTheDocs) for 
more detailed information (under active development).

Once both RethinkDB and BanzaiDB are installed and the configuration is set::

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



.. _RethinkDB: http://www.rethinkdb.com
.. _NoSQL: http://nosql-database.org
.. _Banzai NGS pipeline: https://github.com/mscook/Banzai-MicrobialGenomics-Pipeline
.. _BanzaiDB documentation: http://banzaidb.readthedocs.org
.. _driver performance: http://www.rethinkdb.com/docs/driver-performance/
.. _pip: http://pip.readthedocs.org/en/latest/installing.html
.. _We provide: https://raw.githubusercontent.com/mscook/BanzaiDB/master/misc/python_C++_driver.sh

BanzaiDB Developer HOWTO
========================

In addition to what is described here, `this document by Jeff Forcier`_ and 
`this talk from Carl Meyer`_ provide wonderful footings for developing on/in 
open source projects.


Maintaining a consistent development environment
-------------------------------------------------

**1)** Ensure all development in performed within a virtualenv. A good way too 
bootstrap this is via virtualenv-burrito_.

Execute the installation using::
    
    $ curl -sL https://raw.githubusercontent.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL


**2)** Make a virtualenv called BanzaiDB::

    $ mkvirtualenv BanzaiDB


**3)** Install autoenv_::
    
    $ git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
    $ echo 'source ~/.autoenv/activate.sh' >> ~/.bashrc


Get the current code from GitHub
--------------------------------

Something like this::

    $ cd $PATH_WHERE_I_KEEP_MY_REPOS
    $ git clone https://github.com/mscook/BanzaiDB.git


Install dependencies
--------------------

Something like this::

    $ cd BanzaiDB
    $ # Assuming you installed autoenv -
    $ # You'll want to say 'y' as this will activate the virtualenv each time you enter the code directory
    $ # Otherwise -
    $ # workon BanzaiDB 
    $ pip install -r requirements.txt
    $ pip install -r requirements-dev.txt


Familiarise yourself with the code
----------------------------------
 
The BanzaiDB/BanzaiDB.py is the core module. It handles database insertion, 
deletion and updating.

For example::

    $ ~/BanzaiDB/BanzaiDB$ python BanzaiDB.py -h
    usage: BanzaiDB.py [-h] [-v] {init,populate,update,query} ...

    BanzaiDB v 0.1.2 - Database for Banzai NGS pipeline tool (http://github.com/mscook/BanzaiDB)

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


Listing help on populate::

    $ python BanzaiDB.py populate -h
    usage: BanzaiDB.py populate [-h] {qc,mapping,assembly,ordering,annotation} run_path

    positional arguments:
      {qc,mapping,assembly,ordering,annotation}
                        Populate the database with data from the given pipeline step
        run_path              Full path to a directory containing finished experiments from a pipeline run

    optional arguments:
        -h, --help            show this help message and exit


The fabfile (Fabric file) in fabfile directory contains query pre-written 
functions. 

You can list them like this::

    $ ~/BanzaiDB$ fab -l
    Available commands:

        variants.get_variants_by_keyword           Return variants with a match in the "Product" with the regular_expression
        variants.get_variants_in_range             Return all the variants in given [start:end] range (inclusive of)
        variants.plot_variant_positions            Generate a PDF of SNP positions for given strains using GenomeDiagram
        variants.strain_variant_stats              Print the number of variants and variant classes for all strains
        variants.variant_hotspots                  Return the (default = 100) prevalent variant positions
        variants.variant_positions_within_atleast  Return positions that have at least this many variants
        variants.what_differentiates_strains       Provide variant positions that differentiate two given sets of strains


**Note:** python BanzaiDB.py query simply calls the fabfile discussed above. 


Development workflow
--------------------

Use GitHub. You will have already cloned the BanzaiDB repo (if you followed 
instructions above). To make things easier, please fork 
(https://github.com/mscook/BanzaiDB/fork) and update your local copy to point to 
your fork.

Something like this::

    $ # Assuming your fork is like this
    $ # https://github.com/$YOUR_USERNAME/BanzaiDB/
    $ vi .git/config
    $ # Replace:
	$ # url = git@github.com:mscook/BanzaiDB.git
    $ #  with:
    $ # url = git@github.com:$YOUR_USERNAME/BanzaiDB.git

With this setup you will be able to push development changes to your fork and 
submit Pull Requests to the core BanzaiDB repo when you're happy. 

**Important Note:** Upstream changes will not be synced to your fork by 
default. Please, before submitting a pull request please sync your fork with 
any upstream changes (specifically handle any merge conflicts). Info on 
syncing a fork can be found here_.


Code style/testing/Continuous Integration
------------------------------------------

We try to make joining and/or modifying the BanzaiDB project simple.

General:
    * As close to PEP8 as possible but I ain't no Saint. Just a long as it's 
      clean and readable,
    * Using standard lib UnitTest. There are convenience functions 
      check_coverage.sh & tests/run_tests.sh respectively. We would prefer 
      SMART test vs 100 % coverage.

In the master GitHub repository we use hooks that call:
    * landscape.io (code QC)
    * drone.io (continuous integration)
    * ReadTheDocs (documentation building)

.. _virtualenv-burrito: https://github.com/brainsik/virtualenv-burrito
.. _autoenv: https://github.com/kennethreitz/autoenv
.. _here: https://help.github.com/articles/syncing-a-fork
.. _doctest: http://pythontesting.net/framework/doctest/doctest-introduction/

.. _`this document by Jeff Forcier`: http://www.contribution-guide.org
.. _`this talk from Carl Meyer`: http://pyvideo.org/video/2637/set-your-code-free-releasing-and-maintaining-an


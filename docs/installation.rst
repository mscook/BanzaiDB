Installing BanzaiDB
===================

There are a number of ways to install BanzaiDB once you have RethinkDB and 
the RethinkDB python driver installed. See the following for instructions on 
the `installation of RethinkDB`_ and the `RethinkDB python driver`_. We
recommend installing the python driver with the protobuf library that uses 
a C++ backend. There is a script in the root of the BanzaiDB git repository
that can achieve this task.


**Option 1a** (with root/admin)::
    
    $ pip install BanzaiDB

**Option 1b** (as a standard user)::

    $ pip install BanzaiDB --user


**You'll need to have git installed** for the following alternative install 
options. 

**Option 2a** (with root/admin & git)::

    $ cd ~/
    $ git clone git://github.com/mscook/BanzaiDB.git
    $ cd BanzaiDB
    $ sudo python setup.py install

**Option 2b** (standard user & git) **replacing INSTALL/HERE with appropriate**::

    $ cd ~/
    $ git clone git://github.com/mscook/BanzaiDB.git
    $ cd BanzaiDB
    $ echo 'export PYTHONPATH=$PYTHONPATH:~/INSTALL/HERE/lib/python2.7/site-packages' >> ~/.bashrc
    $ echo 'export PATH=$PATH:~/INSTALL/HERE/bin' >> ~/.bashrc
    $ source ~/.bashrc
    $ python setup.py install --prefix=~/INSTALL/HERE/BanzaiDB/  
    

If the install went correctly::

   $ which BanzaiDB
   /INSTALLED/HERE/bin/BanzaiDB
   $ BanzaiDB -h


**Please regularly check back to make sure you're running the most recent 
BanzaiDB version.** You can upgrade like this:


If installed using option 1x::

    $ pip install --upgrade BanzaiDB
    $ # or
    $ pip install --upgrade BanzaiDB --user

If installed using option 2x::

    $ cd ~/BanzaiDB
    $ git pull
    $ sudo python setup.py install
    $ or
    $ cd ~/BanzaiDB
    $ git pull
    $ echo 'export PYTHONPATH=$PYTHONPATH:~/INSTALL/HERE/lib/python2.7/site-packages' >> ~/.bashrc
    $ echo 'export PATH=$PATH:~/INSTALL/HERE/bin' >> ~/.bashrc
    $ source ~/.bashrc
    $ python setup.py install --prefix=~/INSTALL/HERE/BanzaiDB/  


.. _installation of RethinkDB: http://www.rethinkdb.com/docs/install/
.. _RethinkDB python driver: http://www.rethinkdb.com/docs/install-drivers/python/

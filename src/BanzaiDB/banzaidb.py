#!/usr/bin/env python

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

import sys, os, traceback, argparse, time

import glob

import rethinkdb as r
from   rethinkdb.errors import RqlRuntimeError

from BanzaiDB import core
from BanzaiDB import database

"""
BanzaiDB
========

BanzaiDB is a tool for pairing Microbial Genomics Next Generation Sequencing
(NGS) analysis with a NoSQL database. We use the RethinkDB NoSQL database.
"""

__title__         = 'BanzaiDB'
__version__       = '0.1.2'
__description__   = "Database tool for the Banzai NGS pipeline"
__author__        = 'Mitchell Stanton-Cook'
__author_email__  = 'm.stantoncook@gmail.com'
__url__           = 'http://github.com/mscook/BanzaiDB'
__license__       = 'ECL 2.0'

epi = "Licence: %s by %s <%s>" % (__license__,
                                  __author__,
                                  __author_email__)
__doc__ = " %s v%s - %s (%s)" % ( __title__,
                                  __version__,
                                  __description__,
                                  __url__)



def init_database_with_default_tables(args):
    """
    Create a new RethinkDB database

    :param args: an argparse argument (force)
    """
    # Add additional (default) tables here...
    def_tables = ['variants', 'strains', 'ref', 'ref_feat']
    with database.make_connection() as connection:
        try:
            r.db_create(connection.db).run(connection)
            for atable in def_tables:
                r.db(connection.db).table_create(atable).run(connection)
        except RqlRuntimeError:
            print ("Database %s already exists. Use '--force' option to "
                   "reinitialise the database." % (connection.db))
            if args.force:
                print "Reinitialising %s" % (connection.db)
                r.db_drop(connection.db).run(connection)
                r.db_create(connection.db).run(connection)
                for atable in def_tables:
                    r.db(connection.db).table_create(atable).run(connection)
            else:
                sys.exit(1)
        print ("Initalised database %s. %s contains the following tables: "
                "%s" % (connection.db, connection.db, ', '.join(def_tables)))


def populate_database_with_data(args):
    """
    Populate the RethinkDB

    This is essentially a placeholder that directs the input data to its
    specific populate method.

    :param args: an argparse argument (run_type)
    """

    if args.run_type == 'mapping':
        populate_mapping(args)
    else:
        print "Only support mapping data at the moment"
        sys.exit(1)
    sys.exit()


def populate_qc():
    """
    Populate the database with a QC run
    """
    print "NotImplemented yet!"
    sys.exit(1)


def populate_mapping(args):
    """
    Populate database with a mapping run. Only support for Nesoni at the moment

    TODO: This should also handle BWA. Will need to differentiate between
    Nesoni & BWA runs and handle VCF files.

    For speed faster DB inserts-
        * batch size should be about 200 docs,
        * increase concurrency
        * durability="soft" (will miss data if inserting where power off)
        * run(durability="soft", noreply=True) == danger!

    :param args: an argparse argument (run_path) which is the full path as a
                 string to the Banzai run (inclusive of $PROJECTBASE). For
                 example: /$PROJECTBASE/map/$REF.2014-04-28-mon-16-41-51
    """
    run_path = os.path.normpath(os.path.expanduser(args.run_path))
    # TODO - handle '.' in reference
    ref = run_path.split('/')[-1].split('.')[0]
    infiles = glob.glob(run_path+'/*/report.txt')
    ref = os.path.join(run_path+'/', ref+'/reference.gbk')
    with database.make_connection() as connection:
        for report in infiles:
            parsed = core.nesoni_report_to_JSON(report)
            count = len(parsed)
            if count != 0:
                inserted = r.table('variants').insert(parsed).run(connection)
                strain_JSON = {"StrainID": parsed[0]['StrainID'],
                            "VarCount": count,
                            "id": parsed[0]['StrainID']}
                inserted = r.table('strains').insert(strain_JSON).run(connection)
            else:
                print "No variants for %s. Skipped" % (report)
                s = report.split('/')[-2]
                strain_JSON = {"StrainID" : s,
                            "VarCount" : 0,
                            "id" : s}
                inserted = r.table('strains').insert(strain_JSON).run(connection)
        # Now, do the reference
        ref, ref_meta = core.reference_genome_features_to_JSON(ref)
        inserted = r.table('ref').insert(ref).run(connection)
        inserted = r.table('ref_feat').insert(ref_meta).run(connection)


def populate_assembly():
    """
    Populate the database with an assembly run
    """
    print "NotImplemented yet!"
    sys.exit(1)


def populate_ordering():
    """
    Populate the database with an ordering run
    """
    print "NotImplemented yet!"
    sys.exit(1)


def populate_annotation():
    """
    Populate the database with an ordering run
    """
    print "NotImplemented yet!"
    sys.exit(1)


def updateDB(args):
    """
    Update a DB -> should this be possible?

    Perhaps update should mean add a "run" and make it the active one?
    """
    print "NotImplemented yet!"
    sys.exit(1)


def db_query(args):
    """
    List available (via fab) or provide a ReQL query function
    """
    if args.list:
        fab_loc = os.path.dirname(os.path.realpath(__file__)).split(
            "EGG-INFO/scripts")[0]+'BanzaiDB/fabfile/'
        os.system("fab -f '"+fab_loc+"' -l")
        print '\n\nData can be queried using the following:\n'
        print "\t fab -f '"+fab_loc+"' $COMMAND"

        sys.exit()
    if args.ReQL != '':
        print "Not implemented yet"
        sys.exit()


def create_parser():
    """
    Create the CLI parser

    :returns: a parser with subparsers: init, populate, update & query --------
    """
    parser = argparse.ArgumentParser(description=__doc__, epilog=epi)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='verbose output')
    subparsers = parser.add_subparsers(help='Available commands:')
    init_p = subparsers.add_parser('init', help='Initialise a DB')
    init_p.add_argument('--force', action='store_true', default=False,
                        help=('Reinitilise a database & tables even if '
                              'already exists'))
    populate_p = subparsers.add_parser('populate',
                                       help=('Populates a database with '
                                             'results of an experiment'))
    populate_p.add_argument('run_type', action='store',
                            choices=('qc', 'mapping', 'assembly', 'ordering',
                                     'annotation'),
                            help=('Populate the database with data from the '
                                  'given pipeline step'))
    populate_p.add_argument('run_path', action='store',
                            help=('Full path to a directory containing '
                                  'finished experiments from a pipeline run'))
    update_p = subparsers.add_parser('update', help=('Updates a database '
                                                     'with results from a '
                                                     'new experiment'))
    update_p.add_argument('run_type', action='store',
                          choices=('qc', 'mapping', 'assembly', 'ordering',
                                   'annotation'),
                          help=('Populate the database with data from the '
                                'given pipeline step'))
    update_p.add_argument('run_path', action='store',
                          help=('Full path to a directory containing finished '
                                'experiments from a pipeline run'))
    query_p = subparsers.add_parser('query', help=('List available or provide '
                                                   'database query functions'))
    query_p.add_argument('-l', '--list', action='store_true',
                         default=False, help='List the pre-defined queries')
    query_p.add_argument('-r', '--ReQL', action='store', default='',
                         help='A ReQL statement')
    init_p.set_defaults(func=init_database_with_default_tables)
    populate_p.set_defaults(func=populate_database_with_data)
    update_p.set_defaults(func=updateDB)
    query_p.set_defaults(func=db_query)
    return parser


def main():
    """
    Main function - essentially calls the CLI parser & directs execution
    """
    try:
        start_time = time.time()
        parser = create_parser()
        args = parser.parse_args()
        if args.verbose:
            print "Executing @ " + time.asctime()
        args.func(args)
        if args.verbose:
            print "Ended @ " + time.asctime()
            print 'Exec time minutes %f:' % ((time.time() - start_time) / 60.0)
        sys.exit(0)
    except KeyboardInterrupt, e:
        # Ctrl-C
        raise e
    except SystemExit, e:
        # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

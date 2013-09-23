#!/usr/bin/env python

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


import sys, os, traceback, argparse, time

import rethinkdb as r
from   rethinkdb.errors import RqlRuntimeError, RqlDriverError

import glob
import pickle

import config
import database
import core
import fetch
import query_functions
import misc
import imaging

"""
BanzaiDB
========

Query Banzai NGS pipeline results intelligently and efficiently
"""

__title__         = 'BanzaiDB'
__version__       = '0.1'
__description__   = "Database for Banzai NGS pipeline tool"
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


def make_connection():
    """
    Make a connection to the RethinkDB
    """
    cfg = config.BanzaiDBConfig()
    try:
        connection = r.connect(host=cfg['db_host'], port=cfg['port'], 
                            db=cfg['db_name'])
    except RqlDriverError:
        print "No database connection could be established."
        sys.exit(1)
    return connection


def init_database_with_default_tables(args):
    """
    Create a new RethinkDB database
    """
    # Add additional (default) tables here...
    def_tables = ['variants', 'strains', 'ref', 'ref_feat']
    cfg = config.BanzaiDBConfig()
    connection = r.connect(host=cfg['db_host'], port=cfg['port'])
    try:
        r.db_create(cfg['db_name']).run(connection)
        for atable in def_tables:
            r.db(cfg['db_name']).table_create(atable).run(connection)
    except RqlRuntimeError:
        print "Database %s already exists. " % (cfg['db_name'])
        if args.force:
            print "Reinitialising %s" % (cfg['db_name'])
            r.db_drop(cfg['db_name']).run(connection)
            r.db_create(cfg['db_name']).run(connection)
            for atable in def_tables:
                r.db(cfg['db_name']).table_create(atable).run(connection)
        else:
            connection.close()
            sys.exit(1)
    print ("Initalised database %s. %s contains the following tables: "
            "%s" % (cfg['db_name'], cfg['db_name'], ', '.join(def_tables)))
    connection.close()


def populate_database_with_data(args):
    """
    Populate the RethinkDB
    """
    
    if args.run_type == 'mapping':
        populate_mapping(args)
    sys.exit()
    


def populate_qc():
    pass


def populate_mapping(args):
    """
    Populate database with Nesoni mapping run
    """
    connection = make_connection()
    clean_path = os.path.normpath(os.path.expanduser(args.run_path))
    search     = clean_path.split('/')[-1]
    clean_path = clean_path+'/pbs/'
    ref, output = '', []
    infiles = glob.glob(clean_path+"*"+search+"*")
    for idx, file in enumerate(infiles):
        with open(file) as fin:
            fin.readline()
            fin.readline()
            cur = fin.readline().split(' ')[-1].strip()+'/report.txt'
            output.append(cur)
            if idx == 0:
                ref = fin.readline().split(' ')[-2]+'/reference.gbk'
    # Have all the reports & reference now
    for report in output:
        parsed = core.nesoni_report_to_JSON(report)
        count = len(parsed)
        if count != 0:
            # For speed inserts- 
            #   batch size should be about 200 docs, 
            #   increase concurrency
            #   durability="soft"
            #   run(durability="soft", noreply=True)
            inserted = r.table('variants').insert(parsed).run(connection)
            strain_JSON = {"StrainID" : parsed[0]['StrainID'],
                          "VarCount" : count}
            inserted = r.table('strains').insert(strain_JSON).run(connection)
        else:
            print "No variants for %s. Skipped" % (report)
            s = report.split('/')[-2]
            strain_JSON = {"StrainID" : s,
                          "VarCount" : 0}
    # Now, do the reference
    ref, ref_meta = core.reference_genome_features_to_JSON(args.reference)
    inserted = r.table('ref').insert(ref).run(connection)
    inserted = r.table('ref_feat').insert(ref_meta).run(connection)
    references_coll.insert(ref)


def populate_assembly():
    pass

def populate_ordering():
    pass

def populate_annotation():
    pass




def updateDB(args):
    """
    Not implemented yet!
    """
    pass

def queryDB(args):
    """
    Examples:
        * db.collection.find( <query>, <projection> ) 
        * #database.create_search_index(cfg, 'VARIANTS', 'CDS')
    """
    cfg = config.BanzaiDBConfig()
    try:
        connection = r.connect(host=cfg['db_host'], port=cfg['port'], 
                            db=cfg['db_name'])
    except RqlDriverError:
        print "No database connection could be established."
    exit() 
    ### Howto plot SNPS
    ##SNP_positions = query_functions.get_SNP_positions(cfg, 'S77EC', [1, 1000000])
    ##feat = []
    ##for pos in SNP_positions:
    #    feat.append(misc.create_feature(pos, pos, "SNP", strand=None))
    ##imaging.plot_SNPs(feat)
    ### Howto get CDS core alignment
    query_functions.get_core_alignment(cfg)
    sys.exit()
    if not os.path.isfile(cfg['db_all']+'.ns'):
        print "Database missing. Please use create"
        sys.exit(1)
    if args.mongo != '':
        pass
    elif args.locus_tag != '':
        from collections import Counter
        # Get all required collections
        snp_coll = database.get_collection(cfg, 'VARIANTS')
        ref_features_coll = database.get_collection(cfg, 'REF_FEAT')
        strains_coll = database.get_collection(cfg, 'STRAINS')
        # Get all stored strains and store
        strains = []
        for strain in strains_coll.find({}, {"StrainID" : 1, "_id" : 0}):
            strains.append(strain.values()[0])
        # Get the CDS sequence, product for refernce(LocusTag) and store
        dat = ref_features_coll.find_one({"LocusTag": args.locus_tag}, {"Sequence" : 1, "Product" : 1, "_id" : 0})
        sequence = list(dat['Sequence'])
        product  = dat['Product']
        # Find all SNPs with given LocusTag for given strain. Use PQL
        for strain in strains:
            occur_pos, occur_type, occur_stype, occur_strain = [], [], [], []
            query =  pql.find("StrainID == '"+strain+"' and LocusTag == '"+args.locus_tag+"'")
            # Build up the allele sequence
            cur_seq = list(sequence)
            for idx, snp in enumerate(snp_coll.find(query)):
                # Sanity check
                #print snp
                if snp['RefBase'] != sequence[snp['CDSBaseNum']-1]:
                    print "Error- Sanity check failed"
                else:
                    cur_seq[snp['CDSBaseNum']-1] = snp['ChangeBase']
            print ">%s %s (%s)" % (strain, args.locus_tag, product)
            print ''.join(cur_seq)
            #    occur_pos.append(snp['CDSBaseNum'])
            #    occur_type.append(snp['Class'])
            #    occur_stype.append(snp['SubClass'])
            #    occur_strain.append(snp['StrainID'])
            #tv = idx+1
            #print "General Statistics: %s (%s)" % (args.locus_tag, product)
            #print 40*'-'
            #print "Total variants: %i" % (tv)
            #classes = Counter(occur_type)
            #k, v = classes.keys(), classes.values()
            #print "Variant class population:"
            #for idx, e in enumerate(k):
            #    print "\t"+e , (v[idx]/float(tv))*100
            #print Counter(occur_pos)
        #print Counter(occur_stype)
        #print Counter(occur_strain)
        #db.users.find({'name': {'$regex': 'sometext'}})
        #print snp
        #ref_meta = database.get_collection(cfg, 'REF_FEAT')
        #
        #x = ref_meta.find({"LocusTag": args.locus_tag})
        #for e in x:
        #    print e

    else:
        "No query provided"


def db_query(args):
    """
    List available (via fab) or provide a ReQL query function
    """
    if args.list:
        sys.path.insert(0, "../")
        print 'Data can be queried using the following:'
        os.system("fab -l")
        sys.exit()
    if arg.ReQL != '':
        print "Not implemented yet"
        sys.exit()

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=__doc__, epilog=epi)
        parser.add_argument('-v', '--verbose', action='store_true',
                                        default=False, help='verbose output')
        subparsers = parser.add_subparsers(help='Available commands:') 
        init_parser   = subparsers.add_parser('init', help='Initialise a DB')
        init_parser.add_argument('--force', action='store_true',
                    default=False, help=('Reinitilise a database & tables '
                        'even if already exists'))
        populate_parser = subparsers.add_parser('populate', help=('Populates '
                            'a database with results of an experiment'))
        populate_parser.add_argument('run_type',action='store',
                    choices=('qc', 'mapping', 'assembly', 'ordering', 
                            'annotation'),
                    help=('Populate the database with data from the given '
                          'pipeline step'))
        populate_parser.add_argument('run_path',action='store',
                    help=('Full path to a directory containing finished ' 
                        'experiments from a pipeline run'))
        update_parser = subparsers.add_parser('update', help=('Updates a '
                        'database with results from a new experiment'))
        update_parser.add_argument('run_type',action='store',
                    choices=('qc', 'mapping', 'assembly', 'ordering', 
                            'annotation'),
                    help=('Populate the database with data from the given '
                          'pipeline step'))
        update_parser.add_argument('run_path',action='store',
                    help=('Full path to a directory containing finished ' 
                        'experiments from a pipeline run'))
        query_parser = subparsers.add_parser('query', help=('List available '
                            'or provide database query functions'))
        query_parser.add_argument('-l', '--list', action='store_true', 
                    default=False, help='List the pre-defined queries')
        query_parser.add_argument('-r','--ReQL',action='store', default='',
                    help='A ReQL statement')
        init_parser.set_defaults(func=init_database_with_default_tables)
        populate_parser.set_defaults(func=populate_database_with_data)
        update_parser.set_defaults(func=updateDB)
        query_parser.set_defaults(func=db_query)
        args = parser.parse_args()
        if args.verbose:
            print "Executing @ " + time.asctime()
        args.func(args)
        if args.verbose:
            print "Ended @ " + time.asctime()
            print 'Exec time minutes %f:' % ((time.time() - start_time) / 60.0)
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

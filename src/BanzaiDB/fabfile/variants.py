from collections import Counter
import threading
import ast
import sys

import rethinkdb as r
from   fabric.api   import task

from BanzaiDB import config
from BanzaiDB import converters
from BanzaiDB import misc
from BanzaiDB import imaging

TABLE = 'variants'


def make_a_connection():
    """
    Make a connection to the RethinkDB using defaults or user supplied
    """
    # Get required config - cfg['db_host'], cfg['port'], cfg['db_name']
    cfg = config.BanzaiDBConfig()
    # Make a connection
    try:
        conn = r.connect(host=cfg['db_host'], port=cfg['port'],
                            db=cfg['db_name'])
    except RqlDriverError:
        print "No database connection could be established."
        sys.exit(1)
    return conn

def get_required_strains(strains):
    """
    """
    conn = make_a_connection()
    if strains == None:
        get_strains = r.table('strains').pluck('StrainID').run(conn)
        strains = [e['StrainID'].encode('ascii','ignore') for e in get_strains]
    else:
        strains = strains.split(' ')
    conn.close()
    return strains

def get_num_strains():
    """
    Get the number of strains in the study
    """
    strains = get_required_strains(None)
    strain_count = len(strains)
    conn = make_a_connection()
    # In case reference included in run
    ref_id = list(r.table('ref').run(conn))[0]['id']
    for e in strains:
        if e.find(ref_id) != -1:
            strain_count = strain_count-1
            break
    return strain_count

def filter_counts(list_of_elements, minimum):
    """
    """
    counts = Counter(list_of_elements)
    # Filter out those below threshold
    lookup = {}
    for k, v in counts.items():
        if v >= minimum:
            lookup[k] = v
    return lookup



class ThreadedPositionCounter(threading.Thread):

    def __init__(self, strains):
        threading.Thread.__init__(self)
        self.strains = strains
        self.passed  = None

    def run(self):
        conn = make_a_connection()
        pos = []
        for strain in self.strains:
            cursor = r.table(TABLE).filter({'StrainID': strain}).pluck('Position').run(conn)
            cur = [strain['Position'] for strain in cursor]
            pos = pos+cur
        passed = filter_counts(pos, len(self.strains)).keys()
        self.passed = passed
        conn.close()

def fetch_given_strain_position(strain, position):
    """
    """
    conn = make_a_connection()
    result = list(r.table(TABLE).filter({'StrainID': strain, 'Position': position}).run(conn))[0]
    print str(result['Position'])+","+result['LocusTag']+","+result['Product']+","+result['Class']+","+str(result['SubClass'])
    conn.close()
    return result


@task
def get_variants_in_range(start, end, verbose=True,
                    plucking = 'StrainID Position LocusTag Class SubClass'):
    """
    Return all the variants in given [start:end] range (inclusive of)

    By default: print (in CSV) results with headers:
    StrainID, Position, LocusTag, Class, SubClass

    :param start: the genomic location start
    :param end: the genomic location end
    :param verbose: [def = True] toggle if printing results
    :param plucking: [def = 'StrainID Position LocusTag Class SubClass']
                     toggle headers based on table values

    :returns: List containing JSON elements with the data: 'StrainID',
                'Position', 'LocusTag', 'Class', 'SubClass' for each result
    """
    verbose = ast.literal_eval(str(verbose))
    plucking = plucking.split(' ')
    ROW = 'Position'
    conn = make_a_connection()
    cursor = r.table(TABLE).filter(
                r.row[ROW] <= int(end)).filter(
                r.row[ROW] >= int(start)).pluck(
                        plucking).run(conn)
    JSON_result = []
    for idx, document in enumerate(cursor):
        if verbose:
            if idx != 0:
                print converters.convert_from_JSON_to_CSV(document)
            else:
                print converters.convert_from_JSON_to_CSV(document, True)
        JSON_result.append(document)
    return JSON_result


@task
def get_variants_by_keyword(regular_expression, ROW='Product', verbose=True,
                plucking = 'StrainID Position LocusTag Class SubClass'):
    """
    Return variants with a match in the "Product" with the regular_expression

    Supported regular expression syntax:
    https://code.google.com/p/re2/wiki/Syntax

    By default: print (in CSV) results with headers:
    StrainID, Position, LocusTag, Class, SubClass

    :param regular_expression:
    :param ROW: [def = 'Product'] toggle searching of other table headers
    :param verbose: [def = True] toggle if printing results
    :param plucking: [def = 'StrainID Position LocusTag Class SubClass']
                    toggle headers based on table headers

    :returns: List containing JSON elements with the data: 'StrainID',
                'Position', 'LocusTag', 'Class', 'SubClass' for each result
    """
    verbose = ast.literal_eval(str(verbose))
    plucking = plucking.split(' ')
    conn = make_a_connection()
    cursor = r.table(TABLE).filter(lambda row:row[ROW].match(
                regular_expression)).pluck(plucking).run(conn)
    JSON_result = []
    for idx, document in enumerate(cursor):
        if verbose:
            if idx != 0:
                print converters.convert_from_JSON_to_CSV(document)
            else:
                print converters.convert_from_JSON_to_CSV(document, True)
        JSON_result.append(document)
    return JSON_result


@task
def plot_variant_positions(strains):
    """
    Generate a PDF of SNP positions for given strains using GenomeDiagram

    Places the reference features on the outerring

    User has to provide a space dlimited list of strains (see warning below)

    .. warning: if you have heaps of variants this will most likely fry you
                computer.

    """
    if strains.lower() == 'all':
        strains = None
    strains = get_required_strains(strains)
    conn = make_a_connection()
    gd_data = []
    for strain in strains:
        hits = r.table(TABLE).filter(lambda row:row['StrainID'].match(strain)).pluck('Position','Class').run(conn)
        feat = []
        for hit in hits:
            cur = hit['Position']
            feat.append(misc.create_feature(cur, cur, hit['Class'], strand=None))
        gd_data.append(feat)
    imaging.plot_SNPs(gd_data, strains)

@task
def variant_hotspots(most_prevalent=100, verbose=True):
    """
    Return the (default = 100) prevalent variant positions

    Example usage::

        fab variants.variant_hotspots
        fab variants.variant_hotspots:250

    :param most_prevalent: [def = 100]
    """
    verbose = ast.literal_eval(str(verbose))
    most_prevalent = int(most_prevalent)
    conn = make_a_connection()
    ROW = 'Position'
    # Fetch & store all positions
    cursor = r.table(TABLE).pluck(ROW).run(conn)
    positions = [int(e[ROW]) for e in cursor]
    # Count occurences at positions
    counts = Counter(positions)
    mp = counts.most_common(most_prevalent)
    # Now extract out
    header = "Counts,Position,LocusTag,Product"
    results = []
    results.append(header)
    if verbose:
        print header
    for element in mp:
        first_hit = list(r.table(TABLE).filter(r.row[ROW] == int(element[0])).pluck('Position', 'LocusTag').run(conn))[0]
        product = '"'+list(r.table('ref_feat').filter({'LocusTag' : first_hit['LocusTag']}).pluck('Product').run(conn))[0]['Product']+'"'
        cur = '%i,%i,%s,%s' % (element[1], first_hit['Position'], first_hit['LocusTag'], product)
        results.append(cur)
        if verbose:
            print cur
    conn.close()
    return results

@task
def variant_positions_within_atleast(minimum_at_position=None, verbose=True):
    """
    Return positions that have at least this many variants

    By default the minimum number will be equal to all the strains in the
    study.

    Example usage:

        fab variants.variant_positions_within_atleast
        fab variants.variant_positions_within_atleast:16

    :param minimum_at_position: [def = None] minimum number of variants
                                conserved in N strains at this positions
    """
    verbose = ast.literal_eval(str(verbose))
    if minimum_at_position == None:
        minimum_at_position = get_num_strains()
    else:
        minimum_at_position = int(minimum_at_position)
    conn = make_a_connection()
    ROW = 'Position'
    # Fetch & store all positions
    cursor = r.table(TABLE).pluck(ROW).run(conn)
    positions = [int(e[ROW]) for e in cursor]
    # Count occurences at positions
    counts = Counter(positions)
    # Filter out those below threshold
    lookup = {}
    for k, v in counts.items():
        if v >= minimum_at_position:
            lookup[k] = v
    # Now extract out
    header = "Position,LocusTag,Product"
    results = []
    results.append(header)
    if verbose:
        print header
    for element in lookup:
        first_hit = list(r.table(TABLE).filter(r.row[ROW] == int(element)).pluck('Position', 'LocusTag').run(conn))[0]
        product = '"'+list(r.table('ref_feat').filter({'LocusTag' : first_hit['LocusTag']}).pluck('Product').run(conn))[0]['Product']+'"'
        cur = '%i,%s,%s' % (first_hit['Position'], first_hit['LocusTag'], product)
        results.append(cur)
        if verbose:
            print cur
    conn.close()
    return results

@task
def strain_variant_stats(strains=None, verbose=True):
    """
    Print the number of variants and variant classes for all strains

    Example usage::

        fab variants.strain_variant_stats
        fab variants.strain_variant_stats:'AEXT01-FSL-S3-026 QMA0306.gz'

    :param strains: [def = None] Print info about all strains unless given a
                    space delimited list of specific strains
    :param verbose: [def = True] print to STDOUT

    :returns: a list of results in CSV
    """
    verbose = ast.literal_eval(str(verbose))
    conn = make_a_connection()
    ROW = 'StrainID'
    strains = get_required_strains(strains)
    header = "StrainID,Total Variants,Substitution,Insertion,Deletion"
    results = []
    results.append(header)
    if verbose:
        print header
    for strain in strains:
        tmp = []
        tmp.append(r.table(TABLE).filter({'StrainID': strain}).count().run(conn))
        classes = ['substitution', 'insertion', 'deletion']
        for c in classes:
            tmp.append(r.table(TABLE).filter({'StrainID': strain,
                                              'Class': c}).count().run(conn))
        cur = "%s,%i,%i,%i,%i" % (strain, tmp[0], tmp[1], tmp[2], tmp[3])
        if verbose:
            print cur
        results.append(cur)
    conn.close()
    return results

@task
def what_differentiates_strains(strain_set1, strain_set2, verbose=True):
    """
    Provide variant positions that differentiate two given sets of strains

    Variants positions in strains_set1 not in strain_set2

    This uses threading. Very cool. See:
    stackoverflow.com/questions/2846653/python-multithreading-for-dummies
    """
    strain_set1, strain_set2 = strain_set1.split(' '), strain_set2.split(' ')
    thread1 = ThreadedPositionCounter(strain_set1)
    thread2 = ThreadedPositionCounter(strain_set2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    res1 = sorted(list(set(thread1.passed) - set(thread2.passed)))
    res2 = sorted(list(set(thread2.passed) - set(thread1.passed)))
    conn = make_a_connection()
    results = []
    header = 'Exclusivity,Position,LocusTag,Product,Class,SubClass'
    results.append(header)
    if verbose:
        print header
    for res in res1:
        cur = list(r.table(TABLE).filter({'StrainID': strain_set1[0],'Position': res}).run(conn))[0]
        cur_str = '"%s",%i,%s,"%s",%s,%s' % (' '.join(strain_set1),
                                                cur['Position'],
                                                cur['LocusTag'],
                                                cur['Product'],
                                                cur['Class'],
                                                cur['SubClass'])
        results.append(cur_str)
        if verbose:
            print cur_str
        print cur_str
    for res in res2:
        cur = list(r.table(TABLE).filter({'StrainID': strain_set2[0],'Position': res}).run(conn))[0]
        cur_str = '"%s",%i,%s,"%s",%s,%s' % (' '.join(strain_set2),
                                                cur['Position'],
                                                cur['LocusTag'],
                                                cur['Product'],
                                                cur['Class'],
                                                cur['SubClass'])
        results.append(cur_str)
        if verbose:
            print cur_str

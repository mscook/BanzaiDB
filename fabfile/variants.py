import rethinkdb as r
from   rethinkdb.errors import RqlRuntimeError, RqlDriverError
from   fabric.api   import task
from   fabric.tasks import Task

from BanzaiDB import config
from BanzaiDB import converters
from BanzaiDB import misc
from BanzaiDB import imaging

from collections import Counter
import ast 

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


class CustomTask(Task):
    def __init__(self, func, myarg, *args, **kwargs):
        super(CustomTask, self).__init__(*args, **kwargs)
        self.func = func
        self.myarg = myarg

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)

@task(task_class=CustomTask, myarg='value', alias='at')
def actual_task():
    pass



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
def plot_variant_positions(strains, ROW='StrainID', plucking = ['Position']):
    """
    Generate a PDF of SNP positions for 1 or more strains using GenomeDiagram
    
    Needs a lot of work
    """
    strains = strains.split(' ')
    TABLE = 'variants'
    cfg = config.BanzaiDBConfig()
    try:
        conn = r.connect(host=cfg['db_host'], port=cfg['port'], 
                            db=cfg['db_name'])
    except RqlDriverError:
        print "No database connection could be established."
    gd_data = []
    for strain in strains:
        hits = r.table(TABLE).filter(lambda row:row[ROW].match(strain)).pluck(plucking).run(conn)
        feat = []
        for hit in hits:
            cur = hit['Position']
            feat.append(misc.create_feature(cur, cur, "SNP", strand=None))
        gd_data.append(feat)
    imaging.plot_SNPs(gd_data, strains)

@task
def test(minimum_at_position=1):
    """
    Finish off
    """
    minimum_at_position = int(minimum_at_position)
    TABLE = 'variants'
    ROW = 'Position'
    cfg = config.BanzaiDBConfig()
    try:
        conn = r.connect(host=cfg['db_host'], port=cfg['port'], 
                            db=cfg['db_name'])
    except RqlDriverError:
        print "No database connection could be established."
    #Fetch & store all positions
    positions = []
    hits = r.table(TABLE).pluck('Position').run(conn)
    for hit in hits:
        positions.append(hit['Position'])
    #Count occurences at positions
    counts = Counter(positions)
    lookup = {}
    # Filter out those below threshold
    for k, v in counts.items():
        if v >= minimum_at_position:
            lookup[k] = v
    # Now just need to extract out
    for element in lookup:
        hits = r.table(TABLE).get(filter(r.row[ROW] == int(element)).pluck('Position', 'LocusTag')).run(conn)
        for e in hits:
            print e
            break

@task 
def strain_variant_stats(strains, verbose=True):
    """
    Given some strain identifiers print the number of variants and the classes
    """
    ROW = 'StrainID'
    strains = strains.split(' ')
    conn = make_a_connection()
    header = "StrainID,Total Variants,Substitution,Insertion,Deletion"
    results = []
    results.append(header)
    print header
    for strain in strains:
        tmp = []
        tmp.append(r.table(TABLE).filter({'StrainID': strain}).count().run(conn))
        classes = ['substitution', 'insertion', 'deletion']
        for c in classes:
            #r.table('users').filter({'active': True, 'age': 30}).run(conn)
            tmp.append(r.table(TABLE).filter({'StrainID': strain, 'Class': c}).count().run(conn))
        results.append("%s,%i,%i,%i,%i" % (strain, tmp[0], tmp[1], tmp[2], tmp[3]))
    print results

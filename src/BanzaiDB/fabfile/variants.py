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

from collections import Counter
import ast

import rethinkdb as r
from fabric.api import task

from BanzaiDB import database
from BanzaiDB import converters
from BanzaiDB import misc
from BanzaiDB import imaging

# __version__ = 0.1.2

TABLE = 'variants'


def get_required_strains(strains):
    """
    Returns a list of strains stored in the database if argument strains=None

    If argument strains=None we actually query the database

    If argument strains is not None we actually just spit the strain string on
    the space delimiter.

    :param strains: a string of strain IDs

    :type strains: string or None

    :returns: a list of strains (if None, those all stored in the database)
    """
    strains_list = []
    with database.make_connection() as connection:
        if strains is None:
            get_strains = r.table('strains').pluck('StrainID').run(connection)
            strains_list = [e['StrainID'].encode('ascii', 'ignore') for e in get_strains]
        else:
            strains_list = strains.split(' ')
    return strains_list


def get_num_strains():
    """
    Get the number of strains in the study

    It will query all strains in the database and will factor if the reference
    has been included in the run (will remove it from the count)

    :returns: the number of strains as an int
    """
    strains = get_required_strains(None)
    strain_count = len(strains)
    with database.make_connection() as connection:
        # In case reference is included in run
        # Will need to update for multiple runs
        ref_id = list(r.table('ref').run(connection))[0]['id']
        for e in strains:
            if e.find(ref_id) != -1:
                strain_count = strain_count-1
                break
    return strain_count


def filter_counts(list_of_elements, minimum):
    """
    Filter out elements in a list that are not observed a minimum of times

    :param list_of_elements: a list of for example positions
    :param minimum: the miminum number of times an value must be observed

    :type list_of_elements: list
    :type minimum: int

    :returns: a dictionary of value:observation key value pairs
    """
    counts = Counter(list_of_elements)
    lookup = {}
    for k, v in counts.items():
        if v >= minimum:
            lookup[k] = v
    return lookup


def position_counter(strains):
    """
    Pull all the positions that we observe changes

    .. note::

        This query could be sped up?
    """
    with database.make_connection() as connection:
        pos = []
        for strain in strains:
            # Get every variant position
            cursor = r.table(TABLE).filter({'StrainID': strain}).pluck(
                'Position').run(connection)
            cur = [strain['Position'] for strain in cursor]
            pos = pos+cur
        common = filter_counts(pos, len(strains))
    return common


def fetch_given_strain_position(strain, position):
    """
    With a strainID and a 'change' position return known details

    Prints the position, locus tag, product, class and subclass

    :param strain: the strain ID
    :param position: the position relative to the reference

    :type strain: string
    :type position: int

    :returns: a dictionary (JSON)
    """
    result = {}
    with database.make_connection() as connection:
        result = list(r.table(TABLE).filter({'StrainID': strain, 'Position': position}).run(connection))[0]
        print str(result['Position'])+","+result['LocusTag']+","+result['Product']+","+result['Class']+","+str(result['SubClass'])
    return result


@task
def get_variants_in_range(start, end, verbose=True,
                          plucking='StrainID Position LocusTag Class SubClass'):
    """
    Return all the variants in given [start:end] range (inclusive of)

    By default: print (in CSV) results with headers:
    StrainID, Position, LocusTag, Class, SubClass

    Examples::

        # All variants in the 1Kb range of 60K-61K
        fab variants.get_variants_in_range:60000,61000

        #Nail down on a particular position and redefine the output
        fab variants.get_variants_in_range:60760,60760,plucking='StrainID Position Class Product'

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
    JSON_result = []
    with database.make_connection() as connection:
        cursor = r.table(TABLE).filter(r.row[ROW] <= int(end)).filter(
            r.row[ROW] >= int(start)).pluck(plucking).run(connection)
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
                            plucking='StrainID Position LocusTag Class SubClass'):
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
    JSON_result = []
    with database.make_connection() as connection:
        cursor = r.table(TABLE).filter(lambda row: row[ROW].match(
            regular_expression)).pluck(plucking).run(connection)
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
    gd_data = []
    with database.make_connection() as connection:
        for strain in strains:
            hits = r.table(TABLE).filter(lambda row: row['StrainID'].match(
                strain)).pluck('Position', 'Class').run(connection)
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
    ROW = 'Position'
    # Fetch & store all positions
    with database.make_connection() as connection:
        cursor = r.table(TABLE).pluck(ROW).run(connection)
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
    with database.make_connection() as connection:
        for element in mp:
            first_hit = list(r.table(TABLE).filter(r.row[ROW] == int(element[0])).pluck('Position', 'LocusTag').run(connection))[0]
            product = '"'+list(r.table('ref_feat').filter({'LocusTag': first_hit['LocusTag']}).pluck('Product').run(connection))[0]['Product']+'"'
            cur = '%i,%i,%s,%s' % (element[1], first_hit['Position'], first_hit['LocusTag'], product)
            results.append(cur)
            if verbose:
                print cur
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
    if minimum_at_position is None:
        minimum_at_position = get_num_strains()
    else:
        minimum_at_position = int(minimum_at_position)
    ROW = 'Position'
    # Fetch & store all positions
    with database.make_connection() as connection:
        cursor = r.table(TABLE).pluck(ROW).run(connection)
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
    with database.make_connection() as connection:
        for element in lookup:
            first_hit = list(r.table(TABLE).filter(r.row[ROW] == int(element)).pluck('Position', 'LocusTag').run(connection))[0]
            product = '"'+list(r.table('ref_feat').filter({'LocusTag': first_hit['LocusTag']}).pluck('Product').run(connection))[0]['Product']+'"'
            cur = '%i,%s,%s' % (first_hit['Position'], first_hit['LocusTag'], product)
            results.append(cur)
            if verbose:
                print cur
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
    strains = get_required_strains(strains)
    header = "StrainID,Total Variants,Substitution,Insertion,Deletion"
    results = []
    results.append(header)
    if verbose:
        print header
    with database.make_connection() as connection:
        for strain in strains:
            tmp = []
            tmp.append(r.table(TABLE).filter({'StrainID': strain}).count().run(connection))
            classes = ['substitution', 'insertion', 'deletion']
            for c in classes:
                tmp.append(r.table(TABLE).filter({'StrainID': strain,
                                                  'Class': c}).count().run(connection))
            cur = "%s,%i,%i,%i,%i" % (strain, tmp[0], tmp[1], tmp[2], tmp[3])
            if verbose:
                print cur
            results.append(cur)
    return results


def list_membership(combined, list1, list2):
    """
    """
    in1, in2 = [], []
    for e in combined:
        if e in list1:
            in1.append(e)
        elif e in list2:
            in2.append(e)
        else:
            print "Error"
    return sorted(in1, key=int), sorted(in2, key=int)


def extract_positions(position_list, strain_set, verbose):
    """
    """
    results = []
    with database.make_connection() as connection:
        cursor = r.table(TABLE).get_all(*position_list, index="Position").filter(
            {'StrainID': strain_set[0]}).run(connection)
        for defining_snp in cursor:
            cur = '"%s",%i,%s,"%s",%s,%s' % (' '.join(strain_set),
                                             defining_snp['Position'],
                                             defining_snp['LocusTag'],
                                             defining_snp['Product'],
                                             defining_snp['Class'],
                                             defining_snp['SubClass'])
            results.append(defining_snp)
            if verbose:
                print cur
    return results


@task
def what_differentiates_strains(strain_set1, strain_set2, verbose=True):
    """
    Get variant **positions** that differentiate two given sets of strains

    Example usage::

        fab $BANZAIDB_LOCATION/fabfile/' variants.what_differentiates_strains:ASCC880519,'ASCC881171 ASCC881475'

    :param strain_set1: a space delimited string of strains that belong in set1
    :param strain_set2: a space delimited string of strains that belong in set2

    :returns: 2 lists of JSON that define the variants that are unique to set1
              (1st) and set2 (2nd)
    """
    header = 'Exclusivity,Position,LocusTag,Product,Class,SubClass'
    if verbose:
        print header
    strain_set1, strain_set2 = strain_set1.split(' '), strain_set2.split(' ')
    # Positions only considered if found in all in the strains within the set
    r1, r2 = position_counter(strain_set1), position_counter(strain_set2)
    # A new set with elements in either r1 or r2 but not both
    unique = set(r1).symmetric_difference(set(r2))
    sin1, sin2 = list_membership(unique, r1, r2)
    # if verbose:
    #    print "%i variants are unique to set 1" % (len(sin1))
    #    print "%i variants are unique to set 1" % (len(sin2))
    return (extract_positions(sin1, strain_set1, verbose),
            extract_positions(sin2, strain_set2, verbose))

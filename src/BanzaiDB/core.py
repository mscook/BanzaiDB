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

import sys
import os

from Bio import SeqIO

from BanzaiDB import parsers


#def bring_CDS_to_front(line):
#    """
#
#    """
#    for e in feat_list:
#        if e[]


def nway_reportify(nway_any_file):
    """
    Convert a nway.any to something similar to report.txt

    This converts the nway.any which contains richer information (i.e. N
    calls) into something similar to report.txt

    TODO: Add a simple example of input vs output of this method.

    ref_id, position, strains, ref_base, v_class, changes, evidence,
    consequences

    :param nway_any_file: full path as a string the the file nway.any file

    :type nway_any_file: string

    :returns: a list of tuples. Each list element refers to a variant
              position while the tuple contains the states of each strain
    """
    parsed = []
    nway_any_file = os.path.expanduser(nway_any_file)
    if not os.path.isfile(nway_any_file):
        print "Please specify a valid Nesoni n-way (any) SNP comparison file"
        sys.exit(1)
    else:
        with open(nway_any_file, 'r') as f:
            strains = f.readline().strip().split()[5:-1]
            num_strains = len(strains)/3
            strains = strains[:num_strains]
            for line in f:
                uncalled = False
                cur = line.split("\t")
                ref_id, position, v_class, ref_base = cur[0], int(cur[1]), cur[2], cur[3]
                changes = cur[4:num_strains+4]
                if 'N' in changes:
                    uncalled = True
                evidence = cur[num_strains+4:(2*(num_strains))+4]
                consequences = cur[(2*(num_strains))+4:-1]
                # Something is broken if not true -
                assert len(strains) == len(changes) == len(evidence)
                results = zip([ref_id]*num_strains, [position]*num_strains, strains,
                              [ref_base]*num_strains, [v_class]*num_strains,
                              changes, evidence, consequences,
                              [uncalled]*num_strains)
                parsed.append(results)
        return parsed


def extract_consequences(cons, ftype):
    """
    Extracts out the data from a consequences line

    NOTE: This was originally the core of Nesoni_report_to_JSON. However, as
    v_class is singular BUT substitution states are observed in deletion
    states and other similar we refactored this method out.

    :param cons: a consequences line
    :param ftype: a feature type (substitution, insertion or deletion

    :type cons: string
    :type ftype: string

    :returns: a data list (containing a controlled set of results)
    """
    # May need to add more of these below
    misc_set = ['tRNA', 'gene', 'rRNA']
    # Handle mixed features in the input reference. This nneds to be more
    # generic
    mixed = cons.split(',')
    if len(mixed) == 2:
        # CDS is second
        if mixed[1][1:4] == 'CDS':
            cons = str(mixed[1][1:-1])+", "+mixed[0]+"\n"
    # Work with CDS
    if cons.strip() != '' and cons.split(' ')[0] == 'CDS':
        if ftype.find("substitution") != -1:
            # 0      1         2       3    4      5       6      7
            # class|sub_type|locus_tag|base|codon|region|old_aa|new_aa|
            #   8        9
            # protein|correlated
            dat = ('substitution',) + parsers.parse_substitution(cons)
        elif ftype.find("insertion") != -1:
            dat = ('insertion', None) + parsers.parse_insertion(cons)
        elif ftype.find("deletion") != -1:
            dat = ('deletion', None) + parsers.parse_deletion(cons)
        else:
            raise Exception("Unsupported. Only SNPs & INDELS")
        dat = list(dat)
        dat[3] = int(dat[3])
        dat[4] = int(dat[4])
    elif cons.strip() != '' and cons.split(' ')[0] in misc_set:
        if ftype.find("substitution") != -1:
            dat = (('substitution',) +
                    parsers.parse_substitution_misc(cons))
        elif ftype.find("insertion") != -1:
            dat = (('insertion', None) +
                    parsers.parse_insertion_misc(cons))
        elif ftype.find("deletion") != -1:
            dat = (('deletion', None) +
                    parsers.parse_deletion_misc(cons))
        else:
            raise Exception("Unsupported. Only SNPs & INDELS")
        dat = list(dat)
        dat[3] = int(dat[3])
    else:
        dat = [ftype.split('-')[0]]+[None]*9
    return dat


def nesoni_report_to_JSON(reportified):
    """
    Convert a nesoni nway.any file that has been reportified to JSON

    See: tables.rst for info on what is stored in RethinkDB

    :param reportified: the reportified nway.any file (been through
    nway_reportify()). This is essentially a list of tuples

    :returns: a list of JSON
    """
    stats = {}
    parsed_list = []
    for position in reportified:
        for elem in position:
            skip = False
            ref_id, pos, strain, old, ftype, new, evidence, cons, uncalled = elem
            ref_id = '.'.join(ref_id.split('.')[:-1])
            # Initialise the stats...
            if strain not in stats:
                stats[strain] = 0
            if new == old:
                # Have no change
                #dat = ["conserved"]+[None]*9
                skip = True
            elif new == 'N':
                # Have an uncalled base
                #dat = ["uncalled"]+[None]*9
                skip = True
            # Check for mixtures...
            elif ftype == "substitution" and new.find('-') != -1:
                # Deletion hidden in substitution
                ftype = 'deletion'
                dat = extract_consequences(cons, ftype)
                stats[strain] = stats[strain]+1
            elif ftype == "substitution" and len(new) > 1:
                # Insertion hidden in substitution
                ftype = 'insertion'
                dat = extract_consequences(cons, ftype)
                stats[strain] = stats[strain]+1
            elif ftype == "deletion" and new.find('-') == -1 and len(new) == 1:
                # Substitution hidden in deletions
                ftype = 'substitution'
                dat = extract_consequences(cons, ftype)
                stats[strain] = stats[strain]+1
            elif ftype == "deletion" and new.find('-') == -1 and len(new) > 1:
                # Insertion hidden in deletions
                ftype = 'insertion'
                dat = extract_consequences(cons, ftype)
                stats[strain] = stats[strain]+1
            elif ftype == "insertion" and new.find('-') != -1:
                # Deletion hidden in insertions
                ftype = 'deletion'
                dat = extract_consequences(cons, ftype)
                stats[strain] = stats[strain]+1
            elif ftype == "insertion" and new.find('-') == -1 and len(new) == 1:
                # Substitution hidden in insertions
                ftype = 'substitution'
                dat = extract_consequences(cons, ftype)
                stats[strain] = stats[strain]+1
            # We have the same change state across all strains
            else:
                dat = extract_consequences(cons, ftype)
                stats[strain] = stats[strain]+1
            obs_count = parsers.parse_evidence(evidence)
            # Some simple tests
            the_classes = ['insertion', 'deletion', 'substitution']
            if not skip:
                assert dat[0] in the_classes
                json = {"id": strain+'_'+ref_id+'_'+str(pos),
                        "StrainID": strain,
                        "Position": pos,
                        "LocusTag": dat[2],
                        "Class": dat[0],
                        "SubClass": dat[1],
                        "RefBase": old,
                        "ChangeBase": new,
                        "CDSBaseNum": dat[3],
                        "CDSAANum": dat[4],
                        "CDSRegion": dat[5],
                        "RefAA": dat[6],
                        "ChangeAA": dat[7],
                        "Product": dat[8],
                        "CorrelatedChange": dat[9],
                        "Evidence": obs_count,
                        "UncalledBlock": uncalled
                        }
                parsed_list.append(json)
    return parsed_list, stats


def reference_genome_features_to_JSON(genome_file):
    """
    From genome reference (GBK format) convert CDS, gene & RNA features to JSON

    The following 2 are really good resources:
        * http://www.ncbi.nlm.nih.gov/books/NBK63592/
        * http://www.ncbi.nlm.nih.gov/genbank/genomesubmit_annotation

    .. note:: also see tables.rst for detailed description of the JSON
              schema

    .. warning:: do not think that this handles misc_features

    :param genome_file: the fullpath as a string to the genbank file

    :returns: a JSON representing the the reference and a list of JSON
              containing information on the features
    """
    misc_set = ['tRNA', 'rRNA', 'tmRNA', 'ncRNA']
    with open(genome_file) as fin:
        genome = SeqIO.read(fin, "genbank")
        gd, gn, gid = genome.description, genome.name, genome.id
        print "Adding %s into the RethinkDB instance" % (gd)
        JSON_r = {'revision': int(gid.split('.')[-1]),
                  'reference_name': gd,
                  'id': gn}
        parsed_list = []
        for feat in genome.features:
            start = int(feat.location.start.position)
            JSON_f = {'sequence': str(feat.extract(genome.seq)),
                      'start': start,
                      'end': int(feat.location.end.position),
                      'strand': int(feat.strand),
                      'reference_id': gid,
                      'product': None,
                      'translation': None,
                      'locus_tag': None}
            # Handle CDS, gene, tRNA & rRNA features
            # Do CDS
            if feat.type == 'CDS':
                locus_tag = feat.qualifiers['locus_tag'][0]
                JSON_f['id'] = gid+"_"+locus_tag+"_CDS"
                JSON_f['locus_tag'] = locus_tag
                if 'pseudo' not in feat.qualifiers:
                    JSON_f['translation'] = feat.qualifiers['translation'][0]
                    JSON_f['product'] = feat.qualifiers['product'][0]
                else:
                    JSON_f['product'] = 'pseudo'
                parsed_list.append(JSON_f)
            # Do gene
            elif feat.type == 'gene':
                locus_tag = feat.qualifiers['locus_tag'][0]
                JSON_f['id'] = gid+"_"+locus_tag+"_gene"
                if 'pseudo' not in feat.qualifiers:
                    try:
                        JSON_f['product'] = feat.qualifiers['gene'][0]
                    except:
                        pass
                else:
                    JSON_f['product'] = 'pseudo'
                parsed_list.append(JSON_f)
            # Do other (*RNA)
            elif feat.type in misc_set:
                try:
                    JSON_f['product'] = feat.qualifiers['product'][0]
                except KeyError:
                    JSON_f['product'] = None
                JSON_f['id'] = gid+"_"+str(JSON_f['start'])+"-"+str(JSON_f['end'])
                parsed_list.append(JSON_f)
            else:
                print "Skipped feature at %i to %i " % (JSON_f['start'],
                                                        JSON_f['end'])
        return JSON_r, parsed_list

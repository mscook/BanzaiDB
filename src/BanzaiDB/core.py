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

from Bio import SeqIO

from BanzaiDB import parsers


#def bring_CDS_to_front(line):
#    """
#
#    """
#    for e in feat_list:
#        if e[]


def nesoni_report_to_JSON(report_file):
    """
    Convert a nesoni report.txt to JSON

    **All features in report are parsed**

    See: tables.rst

    :param report_file: fullpath as a string to the report file

    :returns: a list of JSON
    """
    parsed_list = []
    strain = report_file.split('/')[-2]
    misc_set = ['tRNA', 'gene', 'rRNA']
    with open(report_file) as fin:
        print "Parsing %s" % report_file
        # Skip the header
        fin.readline()
        for line in fin:
            ref_id, pos, ftype, old, new, evidence, cons = line.split('\t')
            tmp = ref_id.split('.')
            tmp = '.'.join(tmp[:-1])
            ref_id = tmp
            obs_count = parsers.parse_evidence(evidence)
            # Deal with "mixed" features
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
                            # Support for: 'tRNA', 'gene', 'rRNA'
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
            json = {"id": strain+'_'+ref_id+'_'+pos,
                    "StrainID": strain,
                    "Position": int(pos),
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
                    "Evidence": obs_count
                    }
            parsed_list.append(json)
    print "\t %i variants parsed" % len(parsed_list)
    return parsed_list


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
                JSON_f['product'] = feat.qualifiers['product'][0]
                JSON_f['id'] = gid+"_"+str(JSON_f['start'])+"-"+str(JSON_f['end'])
                parsed_list.append(JSON_f)
            else:
                print "Skipped feature at %i to %i " % (JSON_f['start'],
                                                        JSON_f['end'])
        return JSON_r, parsed_list

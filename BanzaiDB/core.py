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


import parsers
from Bio import SeqIO

def nesoni_report_to_JSON(report_file):
    """
    Convert a nesoni report.txt to JSON

    ** Only CDS features"

    :param report_file: fullpath as a string to the report file
    """
    parsed_list = []
    strain = report_file.split('/')[-2]
    with open(report_file) as fin:
        print "Parsing %s" % report_file
        skip = fin.readline()
        for line in fin:
            ref_id, pos, type, old, new, evidence, cons = line.split('\t')
            tmp = ref_id.split('.')
            tmp = '.'.join(tmp[:-1])
            ref_id = tmp
            obs_count = parsers.parse_evidence(evidence)
            # Only work with CDS
            if cons.strip() != '' and cons.split(' ')[0] == 'CDS':
                if type.find("substitution") != -1:
                    # 0      1         2       3    4      5       6      7
                    #class|sub_type|locus_tag|base|codon|region|old_aa|new_aa|
                    #   8        9
                    #protein|correlated 
                    dat = ('substitution',) + parsers.parse_substitution(cons)
                elif type.find("insertion") != -1:
                    dat = ('insertion', None) + parsers.parse_insertion(cons)
                elif type.find("deletion") != -1:
                    dat = ('deletion', None) + parsers.parse_deletion(cons)
                else:
                    raise Exception("Unsupported. Only SNPs & INDELS")
                json = {"id" : strain+'_'+ref_id+'_'+pos,
                        "StrainID" : strain, 
                        "Position" : int(pos), 
                        "LocusTag" : dat[2],
                        "Class" : dat[0],
                        "SubClass" : dat[1],
                        "RefBase" : old,
                        "ChangeBase" : new,
                        "CDSBaseNum": int(dat[3]),
                        "CDSAANum": int(dat[4]),
                        "CDSRegion": dat[5],
                        "RefAA" : dat[6],
                        "ChangeAA" : dat[7],
                        "Product" : dat[8],
                        "CorrelatedChange" : dat[9],
                        "Evidence" : obs_count
                        }
                parsed_list.append(json)
    return parsed_list


def reference_genome_features_to_JSON(genome_file):
    """
    Given a genome refernce in GenBank format convert CDS features to JSON
    """
    with open(genome_file) as fin:
        genome = SeqIO.read(handle, "genbank")
        reference_name = genome.features[0].qualifiers['organism'][0]
        print "Adding %s into DB" % (reference_name)
        JSON_r = {'RefID' : nucleotide_db_id,
                  'RefName' : reference_name}
        parsed_list = []
        for feat in genome.features:
            # Only get CDS features
            if feat.type == 'CDS':
                dna = str(feat.extract(genome.seq))
                JSON_f = {'LocusTag' : feat.qualifiers['locus_tag'][0],
                          'Sequence' : dna,
                          'Translation' : feat.qualifiers['translation'][0],
                          'Start' : int(feat.location.start.position),
                          'End' : int(feat.location.end.position),
                          'Strand': int(feat.strand),
                          'Product' : feat.qualifiers['product'][0],
                          'RefID': nucleotide_db_id}
                parsed_list.append(JSON_f)
        return JSON_r, parsed_list

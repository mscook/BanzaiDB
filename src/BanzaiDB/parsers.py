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

"""
Functions to parse a nesoni report .txt file
"""


def parse_evidence(evidence):
    """
    From an evidence string/element return a dictionary or obs/counts

    Updated where to handle 0 coverage in an 'N' call! In this case we set
    N = -1

    :param evidence: an evidence string. It looks something like this -
                        Ax27 AGCAx1 AGCAATTAATTAAAATAAx
    """
    obs_count = {}
    elem = evidence.split(' ')
    if elem == ['']:
        obs_count['N'] = -1
    else:
        for e in elem:
            obs, count = e.split('x')
            obs_count[obs] = int(count)
    return obs_count


def strip_non_CDS(protein_line):
    """
    Remove STS/misc_feature etc. from the protein line

    :param protein_line: a parsed protein line as a string
    """
    if protein_line.find(',') != -1:
        protein_line = protein_line.split(',')[0].strip()
    return protein_line


def parse_substitution(consequence):
    """
    Return fields for syn, non-syn or correlated
    """
    elem       = consequence.strip().split(' ')
    correlated = False
    locus_tag  = elem[2]
    base       = int(elem[4])
    codon      = int(elem[6])
    region     = None
    sub_type   = None
    old_aa, new_aa = None, None
    # Handle non-syn
    locus_tag = elem[2]
    if elem[1].find("=>") != -1:
        sub_type = 'non-synonymous'
        old_aa, new_aa = elem[1].split("=>")
        if len(old_aa) == len(new_aa) == 1:
            protein = ' '.join(elem[7:])
        # Need to handle correlated non-syn
        else:
            #CDS YP=>E ECSF_0465 base 379 codon 127 of codons 127..128 hypothetical protein
            #CDS A=>QR ECSF_0595 base 1527 codon 509 apolipoprotein N-acyltransferase
            correlated = True
            if elem[7] == 'of':
                region     = elem[9]
                protein    = ' '.join(elem[10:])
            else:
                protein    = ' '.join(elem[7:])
    # Handle syn
    elif elem[1].find("synonymous") != -1:
        sub_type = 'synonymous'
        protein = ' '.join(elem[7:])
    # Handle correlated (believe these are syn)
    # 2 classes
    # CDS frame-shift LACR_0006 base 526 codon 176 of codons 63..186 XRE family transcriptional regulator
    # CDS frame-shift LACR_0214 base 352 codon 118 hypothetical protein'
    elif elem[1].find("frame-shift") != -1:
        if elem[7] == 'of':
            sub_type = 'synonymous'
            correlated = True
            region     = elem[9]
            protein    = ' '.join(elem[10:])
        else:
            sub_type = 'synonymous'
            correlated = True
            region     = None
            protein    = ' '.join(elem[7:])
    else:
        raise Exception("Error in subsitution", elem)
    # Tidy up possible other features
    protein = strip_non_CDS(protein)
    return sub_type, locus_tag, base, codon, region, old_aa, new_aa, protein, correlated

def parse_substitution_misc(consequence):
    """
    Return fields for syn, non-syn or correlated
    """
    elem       = consequence.strip().split(' ')
    #Default: ['gene', 'G=>A', 'GBS222_0094', 'base', '33']
    correlated = False
    locus_tag  = elem[2]
    # Handle: ['gene', 'C=>G', 'GBS222_t08', 'base', '64,', 'tRNA', 'C=>G', 'GBS222_t08', 'base', '64', 'tRNA-Phe']
    if elem[4][-1] == ',':
        elem[4]= elem[4][:-1]
    base       = int(elem[4])
    codon      = None
    region     = None
    sub_type   = None
    old_aa, new_aa = None, None
    protein = None
    return sub_type, locus_tag, base, codon, region, old_aa, new_aa, protein, correlated


def parse_insertion(consequence):
    # As minimum length can be 7 (but test for 9)
    elem       = consequence.strip().split(' ') + ['', '']
    correlated = False
    locus_tag  = elem[2]
    base       = int(elem[5])
    region     = None
    old_aa, new_aa = None, None
    # Standard. Found two edge cases
    #['CDS', 'frame-shift', 'ECSF_0306', 'before', 'base', '372', '           codon', '124', 'of', 'codons', '124..148', 'truncated', 'propionate', ....]
    #['CDS', 'frame-shift', 'ECSF_1169', 'before', 'base', '1009', 'before', 'codon', '337', 'of', 'codons', '337..466', 'hypothetical', 'protein']
    if elem[1].find("frame-shift") != -1:
        if elem[6] == 'before':
            codon, region, protein = int(elem[8]), elem[11],' '.join(elem[12:])
        elif elem[6] == 'codon':
            codon, region, protein = int(elem[7]), elem[10],' '.join(elem[11:])
        else:
            raise Exception("Error in insertion frame-shift", elem)
    # Correlated. Found 3 edge cases
    #['CDS', 'GYR=>EWQ', 'ECSF_1083', 'before', 'base', '233',            'codon', '78', '  of', 'codons', '78..80', 'putative', 'phage', 'tail', 'component']
    #['CDS', 'TS=>ED',   'ECSF_2797', 'before', 'base', '3730', 'before', 'codon', '1244', 'of', 'codons', '1244..1245', 'hypothetical', 'protein']
    #['CDS', 'T=>NT',   'ECSF_2797',  'before', 'base', '389',            'codon', '130', 'hypothetical', 'protein']
    elif elem[1].find("=>") != -1:
        correlated = True
        old_aa, new_aa = elem[1].split("=>")
        if elem[6] == 'before':
            codon, region, protein = int(elem[8]), elem[11],' '.join(elem[12:])
        elif elem[9] == 'codons':
            codon, region, protein = int(elem[7]), elem[10],' '.join(elem[11:])
        elif elem[6] == 'codon':
            codon, region, protein = int(elem[7]), None,' '.join(elem[8:])
        else:
            raise Exception("Error in insertion correlated", elem)
    # Possibly correlated (Possibly where insertion restores previous deletion)
    # Only 1 edge case. (Did add all 3 above...)
    #['CDS', 'synonymous', 'ECSF_0302', 'before', 'base', '1050', 'codon', '350', 'putative', 'oxidoreductase', '']
    elif elem[1] == 'synonymous':
        correlated = True
        if elem[6] == 'before':
            codon, region, protein = int(elem[8]), elem[11],' '.join(elem[12:])
        elif elem[9] == 'codons':
            codon, region, protein = int(elem[7]), elem[10],' '.join(elem[11:])
        elif elem[6] == 'codon':
            codon, region, protein = int(elem[7]), None,' '.join(elem[8:])
        else:
            raise Exception("Error in insertion possibly correlated", elem)
    else:
        raise Exception("Error in insertion", elem)
    protein = strip_non_CDS(protein)
    return locus_tag, base, codon, region, old_aa, new_aa, protein, correlated


def parse_insertion_misc(consequence):
    elem       = consequence.strip().split(' ') + ['', '']
    # Default: ['gene', '-=>ACC', 'GBS222_0005', 'before', 'base', '105', '', '']
    correlated = False
    locus_tag  = elem[2]
    # Handle: ['gene', 'C=>G', 'GBS222_t08', 'base', '64,', 'tRNA', 'C=>G', 'GBS222_t08', 'base', '64', 'tRNA-Phe']
    if elem[5][-1] == ',':
        elem[5]= elem[5][:-1]
    base       = int(elem[5])
    region     = None
    old_aa, new_aa = None, None
    codon = None
    protein = None
    return locus_tag, base, codon, region, old_aa, new_aa, protein, correlated


def parse_deletion(consequence):
    # As minimum length can be 7 (but test for 9)
    elem = consequence.strip().split(' ') + ['', '']
    correlated = False
    locus_tag  = elem[2]
    base       = int(elem[4])
    codon      = int(elem[6])
    region     = None
    old_aa, new_aa = None, None
    # Standard - found a sinlge edge case...
    # ['CDS', 'frame-shift', 'ECSF_4268', 'base', '691', 'codon', '231', 'of', 'codons', '229..281', 'hypothetical', 'protein']
    # ['CDS', 'frame-shift', 'ECSF_3381', 'base','1692   'codon'  '564' hypothetical protein

    if elem[1].find("frame-shift") != -1:
        if elem[7] == 'of':
            region  = elem[9]
            protein = ' '.join(elem[10:])
        else:
            #Could be correlated...?
            protein = ' '.join(elem[7:])
    # Correlated. Two edge cases
    #['CDS', 'N=>-',     'ECSF_3715', 'base', '235', 'codon', '79', 'hypothetical', 'protein']#
    #['CDS', 'TTS=>XLP', 'ECSF_4010', 'base', '192', 'codon', '64', 'of', 'codons', '64..66', 'phage', 'protein']
    elif elem[1].find("=>") != -1:
        correlated = True
        old_aa, new_aa = elem[1].split("=>")
        if elem[8] == 'codons':
            region = elem[9]
            protein = ' '.join(elem[10:])
        else:
            protein = ' '.join(elem[7:])
    # Possibly correlated (Possibly where insertion effect  downstream deletion)
    #['CDS', 'synonymous', 'L37667', 'base', '979', 'codon', '327', 'of', 'codons', '326..329', 'DNA', 'primase,', 'misc_feature', 'T=>-', 'L37667', 'base', '937', '', '']
    elif elem[1].find("synonymous") != -1:
        correlated = True
        # Think this is WRONG!!!
        old_aa, new_aa = elem[13].split("=>")
        if elem[8] == 'codons':
            region = elem[9]
            protein = ' '.join(elem[10:])
        else:
            raise Exception("New case in deletion", elem)
    else:
        raise Exception("Error in deletion", elem)
    protein = strip_non_CDS(protein)
    return locus_tag, base, codon, region, old_aa, new_aa, protein, correlated


def parse_deletion_misc(consequence):
    elem = consequence.strip().split(' ') + ['', '']
    # Default: ['gene', 'T=>-', 'GBS222_0017', 'base', '366', '', '']
    correlated = False
    locus_tag  = elem[2]
    # Handle: ['gene', 'G=>-', 'GBS222_r08', 'base', '2266,', 'rRNA', 'G=>-', 'GBS222_r08', 'base', '2266', '23S', 'ribosomal', 'RNA', '', '']
    if elem[4][-1] == ',':
        elem[4]= elem[4][:-1]
    base       = int(elem[4])
    codon      = None
    region     = None
    old_aa, new_aa = None, None
    protein = None
    return locus_tag, base, codon, region, old_aa, new_aa, protein, correlated



# Copyright 2013 Mitchell Stanton-Cook Licensed under the
#     Educational Community License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may
#     obtain a copy of the License at
#
#      http://www.osedu.org/licenses/ECL-2.0
#
#     Unless required by applicable law or agreed to in writing,
#     software distributed under the License is distributed on an "AS IS"
#     BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#     or implied. See the License for the specific language governing
#     permissions and limitations under the License.


#https://cgwb.nci.nih.gov/cgi-bin/hgTables?db=hg19&hgta_group=varRep&hgta_track=snp131&hgta_table=snp131&hgta_doSchema=describe+table+schema
#http://alfred.med.yale.edu/alfred/AboutALFRED.asp
#http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=57&ved=0CFYQFjAGODI&url=http%3A%2F%2Fwww.informatics.jax.org%2Fmgihome%2Fnomen%2Fgene.shtml&ei=CqrjUdzoC6XyiAe4rIDoCw&usg=AFQjCNFnXWEFj8RaxoHy8qKiEzIpO2Xl9A&sig2=PJIbHnVQmnE5Fbzb2Tq1DQ&bvm=bv.48705608,d.aGc&cad=rja
#https://github.com/chapmanb/bcbb/tree/master/gff/Scripts/gff

def parse_nway(file_path, strict=True):
    """
    Parses a Nesoni nway file

    Extract out synonymous & non-synonymous, insertions & deletions in 
    **CDS** features only

    Note:
    SNP in feature can be one of (may not be limited to though...):
        ['', 'rRNA', 'tRNA', 'CDS', 'misc_feature', 'STS', 'gene']
    SNP type can be:
        ['synonymous, '=>' (non-synonymous)]
    INDEL type can be:
        ['', 'frame-shift]
    """
    look_up = {'substitution':'snp',
               'insertion-before':'insertion',
               'deletion':'deletion'}
    with open(file_path) as fin:
        strains     = get_strains(fin.readline())
        num_strains = len(strains)
        for line in fin:
            dat = line.split('\t')[0:(3*num_strains+5)]
            position, type, ref_base = dat[1], dat[2], dat[3]
            type  =  look_up[type]
            calls = dat[4:len(strains)+4]
            for idx, strain_base in enumerate(calls):
                if strict and 'N' in calls:
                    break
                cur = ''
                # Do we have a base change
                if strain_base != ref_base:
                    annotation_info = dat[2*len(strains)+idx+4].split(' ')
                    # Handle no annotation
                    try:
                        variant_class = annotation_info[1]
                        feature_type  = annotation_info[0]
                        # Handle overlapping features
                        cds_only = dat[2*len(strains)+idx+4].split(', CDS')
                        if len(cds_only) == 2:
                            tmp = 'CDS'+str(cds_only[-1])
                            annotation_info = tmp.split(' ')
                            variant_class   = annotation_info[1]
                            feature_type    = annotation_info[0]
                    except IndexError:
                        break
                    # Substitution mutation can result in 
                    # synonymous or non-synonymous SNP
                    # It can also be correlated (run of SNP/INDELs)
                    if type == 'snp':
                        # have substitution
                        # synonymous in CDS
                        if (variant_class == "synonymous" and 
                                feature_type == "CDS"):
                                syn_snp(strains[idx], 
                                        int(position), 
                                        ref_base, strain_base, 
                                        feature_type,
                                        annotation_info[2],
                                        int(annotation_info[4]), 
                                        int(annotation_info[6]), 
                                        ' '.join(annotation_info[7:]))
                        # Handle non-synonymous SNP in CDS/correlated
                        elif (variant_class.find("=>") != -1 and 
                                feature_type == "CDS"):
                            old, new = variant_class.split("=>")
                            if len(old) == len(new) == 1:
                                nonsyn_snp(strains[idx], 
                                           int(position),
                                           ref_base, strain_base,
                                           old, new,
                                           feature_type, 
                                           annotation_info[2],
                                           int(annotation_info[4]),
                                           int(annotation_info[6]),
                                           ' '.join(annotation_info[7:]))
                            else:
                                # Have a correlated
                                corr_snp(strains[idx],
                                        int(position),
                                        ref_base, strain_base,
                                        feature_type,
                                        annotation_info[2],
                                        int(annotation_info[4]),
                                        int(annotation_info[6]),
                                        ' '.join(annotation_info[10:]))
                        else:
                            if 'CDS' in annotation_info:
                                if variant_class == 'frame-shift':
                                    corr_snp(strains[idx],
                                             int(position),
                                             ref_base, strain_base,
                                             feature_type,
                                             annotation_info[2],
                                             int(annotation_info[4]),
                                             int(annotation_info[6]),
                                             ' '.join(annotation_info[10:]))
                                else:
                                    print "Skipped: %s %s" % (strains[idx],
                                                              position)
                    # Have INDELs
                    elif type == 'insertion' or type == 'deletion':
                        try:
                            old, new = variant_class.split('=>')
                            if len(old) == len(new) == 1:
                                # Have non-synomous SNP & INDELS at region
                                nonsyn_snp(strains[idx], 
                                           int(position),
                                           ref_base, strain_base,
                                           old, new,
                                           feature_type, 
                                           annotation_info[2],
                                           int(annotation_info[4]),
                                           int(annotation_info[6]),
                                           ' '.join(annotation_info[7:]))
                            else:
                                # Have a standard INDEL
                                # Have some edge cases to deal with
                                # correlated (possibly)
                                try:
                                    if type == 'deletion' and len(old) < len(new):
                                         indel(type, 
                                              strains[idx],
                                              int(position),
                                              ref_base, strain_base,
                                              old, new,
                                              feature_type,
                                              annotation_info[2],
                                              int(annotation_info[4]),
                                              int(annotation_info[6]),
                                              annotation_info[9],
                                              ' '.join(annotation_info[10:]),
                                              corr=True)
                                except
                                   

                                try:
                                    indel(type, 
                                          strains[idx],
                                          int(position),
                                          ref_base, strain_base,
                                          old, new,
                                          feature_type,
                                          annotation_info[2],
                                          int(annotation_info[4]),
                                          int(annotation_info[6]),
                                          annotation_info[9],
                                          ' '.join(annotation_info[10:]))
                                except IndexError:
                                    print type, strains[idx], int(position), annotation_info
                        except ValueError:
                            pass
                            #print type, annotation_info
                            # Could have synomous SNP & INDELS in region
                            #print position, "VC:", variant_class
                            #print position, annotation_info
                        #if variant_class == 'frame-shift':
                        #    pass         
                        #else:
                        #    # correlated
                        #    print "here 3"    
                    
                    elif type == 'insertion':
                        pass
                    else:
                        print "Not handled: %s %s" % (strains[idx], position)



def get_strains(line):
    """
    Returns a list of strain IDs
    """
    number_of_strains = (len(line.split('\t')[4:])-1)/3
    return line.split('\t')[4:(4+number_of_strains)]


def syn_snp(strain, position, ref_base, strain_base, feature, locus_tag,
                    base, codon, protein):
    type          = 'SNP'
    variant_class = 'synonymous'
    print "%s (%s) %s %i %s" % (type, variant_class, strain, 
                                    position, locus_tag)

def nonsyn_snp(strain, position, ref_base, strain_base, 
                     ref_aa, strain_aa, feature, 
                    locus_tag, base, codon, protein):
    type          = 'SNP'
    variant_class = 'non-synonymous'
    print "%s (%s) %s %i %s" % (type, variant_class, strain, 
                                    position, locus_tag)

def corr_snp(strain, position, ref_base, strain_base, feature, 
                    locus_tag, base, codon, protein):
    type          = 'SNP'
    variant_class = 'correlated'
    print "%s (%s) %s %i %s" % (type, variant_class, strain, 
                                    position, locus_tag)

def indel(type, strain, position, ref_bases, strain_bases, 
          ref_aas, strain_aas, feature, locus_tag, base, codon, 
          codon_range, protein, corr=False):
    print type, strain, position, locus_tag
    


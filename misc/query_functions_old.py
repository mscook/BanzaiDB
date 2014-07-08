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


import collections
# import pql

import database

def get_strains(cfg_object, verbose=True):
    """
    Return/list the strains contained in the database

    Collection is 'STRAINS'
    """
    strain_list = []
    strains = database.get_collection(cfg_object, 'STRAINS')
    for s in strains.find({}, {"StrainID" : 1, "_id" : 0}):
        tmp = s.values()[0]
        strain_list.append(tmp)
        if verbose:
            print "%s" % (tmp)
    return strain_list

def get_variant_stats(cfg_object, strain=None):
    """
    Return/list the the stats for the variants

    Collection is 'VARIANTS'
    """
    if strain == None:
        strains = get_strains(cfg_object, False)
    else:
        strains = strain
    variants = database.get_collection(cfg_object, 'VARIANTS')
    for s in strains:
        vclass, vsubclass = [], []
        query =  pql.find("StrainID == '"+s+"'")
        for v in variants.find(query):
            vclass.append(v['Class'])
            vsubclass.append(v['SubClass'])
        vclass_count    = collections.Counter(vclass)
        vsubclass_count = collections.Counter(vsubclass)
        print '%s' % s
        print 'Total variants: %i' % len(vclass)
        for k in vclass_count.keys():
            if k == 'substitution':
                print '\t%s %i (%i non-synonymous)' % (k.title(), vclass_count[k], vsubclass_count['non-synonymous'])
            else:
                print '\t%s %i' % (k.title(), vclass_count[k])
        print '\n'


def get_SNP_positions(cfg_object, strain, range=None):
    """
    Return a list of all SNPs given strain ID. Optionally can provide a range
    """
    SNP_positions = []
    variants = database.get_collection(cfg_object, 'VARIANTS')
    if not range:
        query = pql.find("StrainID == '"+strain+"' and Class == 'substitution'")
    else:
        query = pql.find("StrainID == '"+strain+"' and Class == 'substitution' and (Position >= "+str(range[0])+" and Position <= "+str(range[1])+")")
    print query
    for v in variants.find(query, {"Position" : 1, "_id" : 0}):
        SNP_positions.append(v.values()[0])
    return SNP_positions


def get_core_alignment(cfg_object):
    """
    Build the core alignment (equivalent to the nway, but only CDS)
    """
    num_strains = len(get_strains(cfg_object, False))
    variants  = database.get_collection(cfg_object, 'VARIANTS')
    reference = database.get_collection(cfg_object, 'REF')
    positions_all = []
    # Fetch all substitution positions and store
    query = pql.find("Class == 'substitution'")
    for hit in variants.find(query, {"Position" : 1, "_id" : 0}):
        positions_all.append(hit.values()[0])
    unique_positions = sorted(list(set(positions_all)))
    #TODO TODO TODO - below is a hack. We should really store RefName in each
    # varaiant
    refName = reference.find_one({}, {"RefName": 1,  "_id" : 0}).values()[0]
    # Build the reference align
    print ">% s (reference)" % (refName)
    # Build the reference
    for pos in unique_positions:
        query = pql.find("Class == 'substitution' and Position == "+str(pos))
        print variants.find_one(query)
    #Counnt the frequency at each position
    #    for v in variants.find(query):
    #        vclass.append(v['Class'])
    #        vsubclass.append(v['SubClass'])
    #    vclass_count    = collections.Counter(vclass)
    #    vsubclass_count = collections.Counter(vsubclass)
    #    print '%s' % s
    #    print 'Total variants: %i' % len(vclass)
    #    for k in vclass_count.keys():
    #        if k == 'substitution':
    #            print '\t%s %i (%i non-synonymous)' % (k.title(), vclass_count[k], vsubclass_count['non-synonymous'])
    #        else:
    #            print '\t%s %i' % (k.title(), vclass_count[k])
    #    print '\n'





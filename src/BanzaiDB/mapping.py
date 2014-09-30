# Copyright 2013-2014 Mitchell Stanton-Cook Licensed under the
# Educational Community License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#   http://www.osedu.org/licenses/ECL-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.

import os


def get_depth_cutoff(run_path, sid):
    """
    Read the conensus.log to determine the base calling depth...

    .. note:: not used anymore see: get_N_char_positions
    """
    filename = 'consensus_log.txt'
    cut_off = 0
    with open(os.path.join(os.path.join(run_path, sid), filename)) as fin:
        for line in fin:
            if line.find('base with no errors') != -1:
                cut_off = int(line.split()[0])
                print "Using depth coverage < %iX as missing" % (cut_off)
                return cut_off
        return -1


def get_N_char_positions(run_path, sid):
    """
    Return all the positions of N calls in the consensus.fa
    """
    full, no_call, filename = '', [], 'consensus.fa'
    with open(os.path.join(os.path.join(run_path, sid), filename)) as fin:
        for idx, line in enumerate(fin):
            if not line.startswith('>'):
                full = full+line.strip()
    full = list(full)
    for idx, e in enumerate(full):
        if e == 'N':
            no_call.append(idx)
    return no_call

def get_coverage(run_path, sid):
    """
    Return any abnormal coverage information in the .consequences file
    """
    filename = sid + ".consequences" #change this when we work out naming convention
    strain_features = []

    with open(os.path.join(os.path.join(run_path, sid), filename)) as fin:
        for idx, line in enumerate(fin):
            feature = {}
            if idx >= 1:
                cur = line.split("\t")
                feature['id'] = cur[0]+'_'+sid+'_'+cur[1]
                coverage = float(cur[5])

                # Only store if there is interesting coverage statistics
                if coverage != 1.0: # 
                    feature['coverage'] = coverage

                old_len, new_len = int(cur[2]), int(cur[3])
                AA_len = old_len - new_len
               
                # Only store if there is an indel 
                if AA_len != 0:
                    feature['aa_difference'] = AA_len

                if 'coverage' in feature or 'difference' in feature:
                    feature['StrainID'] = sid 
                    feature['Reference'] = cur[0]
                    feature['LocusTag'] = cur[1]
                    strain_features.append(feature)

    return strain_features

# Copyright 2013-2014 Mitchell Stanton-Cook Licensed under the
# Educational Community License, Version 2.0 (the "License"); you may
# notte_feature use this file except in compliance with the License. You may
# obtain a copy of the License at
#
# http://www.osedu.org/licenses/ECL-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.


from Bio import SeqFeature


def create_feature(begin, end, feat_type, strand=None):
    """
    Creates a BioPython SeqFeature record

    :param begin: where the variant starts
    :param end: where the variaants ends
    :param type: if a substitution or INDEL
    :param strand: [default] None of -1/1

    :type begin: int
    :type end: int
    :type feat_type: string (typically one of insertion, deletion, substitution)
    :type stand: None or int

    :returns: a Bio.SeqFeature object
    """
    location = SeqFeature.FeatureLocation(SeqFeature.ExactPosition(int(begin)),
                                          SeqFeature.ExactPosition(int(end)))
    if strand is not None:
        return SeqFeature.SeqFeature(location, type=feat_type,
                                     strand=int(strand))
    else:
        return SeqFeature.SeqFeature(location, type=feat_type,
                                     strand=strand)

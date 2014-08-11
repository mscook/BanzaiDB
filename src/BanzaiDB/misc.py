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
from itertools import groupby, count


def create_feature(begin, end, feat_type, strand=None):
    """
    Creates a BioPython SeqFeature record

    :param begin: where the variant starts
    :param end: where the variaants ends
    :param type: if a substitution or INDEL
    :param strand: [default] None of -1/1

    :type begin: int
    :type end: int
    :type feat_type: string (typically one of insertion, deletion,
                             substitution)
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


def chunk_list(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


# Below is borrowed from: http://codereview.stackexchange.com/questions/5196/
# grouping-consecutive-numbers-into-ranges-in-python-3-2
def as_range(positions):
    """
    Given a list of positions, merge them into intervals if possible
    """
    l = list(positions)
    if len(l) > 1:
        return '{0}-{1}'.format(l[0], l[-1])
    else:
        return '{0}'.format(l[0])


def get_intervals(ranges):
    """
    Returns a set of intervals in format [(begin, end) ...]
    """
    interval_list = []
    x = ','.join(as_range(g) for _, g in groupby(
        ranges, key=lambda n, c=count(): n-next(c)))
    intervals = x.split(',')
    for idx, e in enumerate(intervals):
        try:
            begin, end = e.split('-')
        except ValueError:
            begin, end = e, e
        begin, end = int(begin), int(end)
        interval_list.append((begin, end))
    return interval_list

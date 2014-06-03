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

from Bio import Entrez, SeqIO


def get_genbank(nucleotide_db_id):
    """
    Given a complete genome identifier (NCBI) return the genome (SeqIO) object
    """
    Entrez.email = "BanzaiDB.user@github.com"
    handle = Entrez.efetch(db="nucleotide", 
                               id=nucleotide_db_id, 
                               rettype="gbwithparts")
    genome = SeqIO.read(handle, "genbank")
    return genome

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


class DNA_BASE:
    """
    A DNA base class
    """
    def __init__(self, strain, position, base):
        self.strain      = strain
        self.position    = position
        self.strain_base = base
        self.ref_base    = base

class DNA_VARIANT(DNA_BASE):
    """
    A DNA variant Class
    """
    def __init__(self, strain, position, ref_base, strain_base, 
                 evidence, annotation):
        self.strain      = strain
        self.position    = position
        self.strain_base = strain_base
        self.ref_base    = ref_base
        self.evidence    = evidence
    
    def __repr__(self):
        return '%s %i %s' % (self.strain, self.position, self.type)

class DNA_SNP(DNA_VARIANT):
    pass

class DNA_INDEL(DNA_VARIANT):
    pass



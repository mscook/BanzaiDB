# Copyright 2013-2014 Mitchell Stanton-Cook Licensed under the
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


class NestedJSONError(Exception):
    """
    The conversion of JSON to CSV does not support nested JSON
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class CouldNotParseJSONError(Exception):
    """
    The conversion only takes a single JSON element, not a list of elements
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class InvalidDBName(Exception):
    """
    RethinkDB only likes database names that match "^[a-zA-Z0-9_]+$"
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)

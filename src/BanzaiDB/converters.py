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

import tablib
import json
import sys

from BanzaiDB import errors


def convert_from_JSON_to_CSV(json_data, header=False):
    """
    Converts a single JSON element to CSV

    .. note:: this will not handle nested JSON. Will need to used something
              like https://github.com/evidens/json2csv to achieve this

    :param json_data: the JSON
    :param header: [optional] include the and return the header
    """
    json_str = json.dumps(json_data)
    data = tablib.Dataset()
    data.json = '['+json_str+']'
    tmp = data.csv.split('\n')
    if tmp[1].find('}') != -1:
        raise errors.NestedJSONError(data.json)
    if tmp[0] and tmp[1] == '':
        raise errors.CouldNotParseJSONError(data.json)
    if header:
        return tmp[0].rstrip()+"\n"+tmp[1].rstrip()
    else:
        return tmp[1].rstrip()


def convert_from_csv_to_JSON(csv_data, header=False):
    """
    Converts from CSV to JSON

    NotImplemented yet!

    :param json_data: csv data
    :param header: [optional]
    """
    sys.stderr.write("NotImplemented yet!")
    sys.exit(1)

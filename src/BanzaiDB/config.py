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


import os
import sys


class BanzaiDBConfig(object):
    """
    BanzaiDB configuration class
    """
    def __init__(self):
        self.config = self.read_config()

    def __getitem__(self, key):
        try:
            return self.config[key]
        except KeyError:
            msg = "Trying to get config option that does not exist.\n"
            sys.stderr.write(msg)
            return None

    def __setitem__(self, key, item):
        allowed = ['db_host', 'port', 'db_name', 'auth_key']
        if key in allowed:
            if key == 'port':
                self.config[key] = int(item)
            else:
                self.config[key] = item
        else:
            raise KeyError('Must be one of '+str(allowed))

    def read_config(self):
        """
        Read a BanzaiDB configuration file

        Currently only supports:
            * db_host  =  [def = localhost]
            * port     =  [def = 28015]
            * db_name  =  [def = Banzai]
            * auth_key =  [def = '']

        .. note:: updated so that "port" is stored as an integer
        """
        cfg = {}
        cfg['db_host'] = 'localhost'
        cfg['port'] = 28015
        cfg['db_name'] = 'Banzai'
        cfg['auth_key'] = ''
        try:
            with open(os.path.expanduser('~/')+'.BanzaiDB.cfg') as fin:
                # sys.stderr.write("Using a BanzaiDB config file\n")
                for line in fin:
                    if (line.startswith('db_host') or
                            line.startswith('port') or
                            line.startswith('db_name') or
                            line.startswith('auth_key')):
                        option, val = line.split('=')
                        option, val = option.strip(), val.strip()
                        if option == 'port':
                            val = int(val)
                        cfg[option] = val
        except IOError:
            sys.stderr.write("Using RethinkDB defaults\n")
        return cfg

    def dump_items(self):
        """
        Returns a string of all configuration options

        :returns: a new line delimited string of all config options
        """
        config_str = ''
        for key, value in self.config.items():
            cur = str(key)+" = "+str(value)+"\n"
            config_str = config_str+cur
        return config_str[:-1]

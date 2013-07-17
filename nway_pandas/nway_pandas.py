#!/usr/bin/env python

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


"""
nway_pandas
===========

Get Nesoni nway into pandas for manipulation
"""

__author__ = "Mitchell Stanton-Cook"
__licence__ = "ECL"
__version__ = "0.1"
__email__ = "m.stantoncook@gmail.com"
epi = "Licence: "+ __licence__ + " by " + __author__ + " <" + __email__ + ">"
USAGE = "nway_pandas -h"


import sys, os, traceback, argparse, time

import parse

def main():
    global args
    args.nway_file = os.path.expanduser(args.nway_file)
    parse.parse_nway(args.nway_file)
    
if __name__ == '__main__':
    try:
        start_time = time.time()
        desc = __doc__.split('\n\n')[1].strip()
        parser = argparse.ArgumentParser(description=desc,epilog=epi)
        parser.add_argument('-n', '--nway_file', action='store',
                            help='[Required] fullpath to the nway file')
        args = parser.parse_args()
        msg = "Missing required arguments.\nPlease run: nway_pandas -h"
        if args.nway_file == None:
            print msg
            sys.exit(1)

        print "Executing @ " + time.asctime()
        main()
        print "Ended @ " + time.asctime()
        print 'total time in minutes:',
        print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

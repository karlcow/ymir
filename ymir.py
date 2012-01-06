#!/usr/bin/env python3
# encoding: utf-8
"""
ylmir.py

Created by Karl Dubost on 2011-12-03.
Copyright (c) 2011 Grange. All rights reserved.
"""

import sys
from optparse import OptionParser


help_message = '''
This script has been entirely created 
for processing text files for the site 
La Grange http://www.la-grange.net/.
'''


def main():

    # Parsing the cli
    usage = "usage: %prog [options] raw_blog_post"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--output", 
                    action="store", type="string", 
                    dest="destination", metavar="DESTINATION", 
                    help="the blog post ready to be sync")
    parser.add_option("--atom", 
                    action="store_true",
                    dest="createfeed",
                    help="create an atom feed. DEFAULT")
    parser.add_option("--noatom", 
                    action="store_false",
                    dest="createfeed",
                    help="do not create the atom feed.")
    parser.set_defaults(createfeed=True)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments. Just enter the raw blog post to process.")
            
if __name__ == "__main__":
    sys.exit(main())

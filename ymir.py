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
    parser = OptionParser()
    parser.add_option("-f", "--file", 
                      action="store", type="string", 
                      dest="source", metavar="SOURCE", 
                      help="The raw blog post to process")
    parser.add_option("-o", "--output", 
                      action="store", type="string", 
                      dest="destination", metavar="DESTINATION", 
                      help="The blog post ready to be sync")
    (options, args) = parser.parse_args()

if __name__ == "__main__":
    sys.exit(main())

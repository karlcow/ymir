#!/usr/bin/env python2.7
# encoding: utf-8
"""
ylmir.py

Created by Karl Dubost on 2011-12-03.
Copyright (c) 2011 Grange. All rights reserved.
"""

import sys
from optparse import OptionParser
from lxml.html import tostring, html5parser
from lxml import etree

# CONFIG 
SITENAME = "Les carnets Web de La Grange"
SITE = "http://www.la-grange.net/"
STATUSLIST = ['draft','pub','acl']
LICENSELIST = {'ccby': 'http://creativecommons.org/licenses/by/2.0/fr/', 
               'copy': '©'}
AUTHOR = "Karl Dubost"
AUTHORURL = "http://www.la-grange.net/karl/"
FEEDIDTAG = "tag:la-grange.net,2000-04-12:karl"
FEEDATOMNOM = "feed.atom"

# CONFIG with cli (TODO)
STYLESHEET = "/2011/12/01/proto/style/article.css"
STATUS = ""
MAXFEEDITEM = 20
LICENSE = "ccby"

# PATHS

help_message = '''
This script has been entirely created 
for processing text files for the site 
La Grange http://www.la-grange.net/.
'''

def isDocHtml5(doctype):
    if doctype == "<!DOCTYPE html>":
        return True
    else:
        return False

def status(doc):
    """Check the publication status of the document"""
    for meta in doc.xpath(".//meta"):
        print meta
        
        # if meta.attrib.has_key('name') and meta.attrib['name'] == 'status':
        #     status = meta.attrib['content']
        #     return status
    
def parserawpost(rawpostpath):
    doc = html5parser.parse(rawpostpath)
    # doctype = doc.docinfo.doctype
    # if isDocHtml5(doctype): 
    #     print "html5 doctype"
    # else:
    #     print "no html5 doctype"
    return doc

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
    rawpostpath = args[0]
    
    rawpost = parserawpost(rawpostpath).getroot()
    print etree.tostring(rawpost)
    for element in rawpost.iter("{http://www.w3.org/1999/xhtml}meta"):
        print "%s - %s" % (element.tag, element.text)
    status(rawpost)
    
if __name__ == "__main__":
    sys.exit(main())


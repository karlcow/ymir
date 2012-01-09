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
HTMLNS = "http://www.w3.org/1999/xhtml"
HTML = "{%s}" % HTMLNS
NSMAP = {None : HTMLNS}

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

def getdocstatus(doc):
    """Check the publication status of the document
    returns a string
    if there are multiple meta, returns the first one and issues a warning"""
    findstatus = etree.ETXPath("//{%s}meta[@name='status']" % HTMLNS)
    if len(findstatus(doc)) > 1:
        print "WARNING: There are more than one status. Taking the first one"
    status = findstatus(doc)[0].attrib['content']
    if status in STATUSLIST:
        print "INFO: The document is a draft"
        return status
    else: 
        sys.exit("ERROR: No valid status for your document")

def gettitle(doc):
    """return an html string being the title of the document"""
    findtitle =  etree.ETXPath("//{%s}h1[text()]" % HTMLNS)
    if len(findtitle(doc)) == 0:
        sys.exit("ERROR: The document has no title")
    title = findtitle(doc)[0]
    return etree.tostring(title, encoding=unicode)    

def parserawpost(rawpostpath):
    """Given a path, parse an html file
    TODO check if the file is correct.
    """
    doc = html5parser.parse(rawpostpath).getroot()
    print "INFO: Document parsed"
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

    # Parse the document    
    rawpost = parserawpost(rawpostpath)
    # Check the status
    STATUS = getdocstatus(rawpost)
    print gettitle(rawpost)


if __name__ == "__main__":
    sys.exit(main())


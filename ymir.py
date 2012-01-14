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
DATETYPELIST = ['created','modified']
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

# General processing features

def gettext(elem):
   """Getting all text from inside an element 
   http://effbot.org/zone/element-bits-and-pieces.htm
   """
   text = elem.text or ""
   for e in elem:
      text += gettext(e)
      if e.tail:
         text += e.tail
   return text

def parserawpost(rawpostpath):
    """Given a path, parse an html file
    TODO check if the file is correct.
    """
    doc = html5parser.parse(rawpostpath).getroot()
    print "INFO: Document parsed"
    return doc

# Extracting information from the blog posts

def getdocstatus(doc):
    """Check the publication status of the document
    returns a string
    if there are multiple meta, returns the first one and issues a warning"""
    findstatus = etree.ETXPath("//{%s}meta[@name='status']" % HTMLNS)
    docstatus = findstatus(doc)
    if len(docstatus) >= 1:
        status = docstatus[0].attrib['content']
        if status in STATUSLIST:
            if len(docstatus) > 1:
                print "WARNING: There are more than one status. Taking the first one : " + status
            else:
                print "INFO: The document status is " + status
            return status
        else: 
            raise Exception, "ERROR: No valid status for your document: %s not in %s" % (status, STATUSLIST)
    if len(docstatus) == 0:
        print "WARNING: There is no status for this document."
        status = "undefined"
        return status

def getdocdate(doc, STATUS, DATETYPE):
    """return the creation date of the document in ISO format YYYY-MM-DD
    Input the document, status, typeofdate in between created and modified"""
    # TODO: check if the format is correct aka YYYY-MM-DD
    if DATETYPE not in DATETYPELIST:
        sys.exit("ERROR: No valid type for the date: " + DATETYPE)            
    if STATUS == "draft":
        finddate = etree.ETXPath("//{%s}meta[@name=%r]" % (HTMLNS,DATETYPE))
        datelist = finddate(doc)
        date = datelist[0].attrib['content']
        if len(datelist) == 1:
            print "INFO: The date is " + date
        elif len(datelist) > 1:
            print "WARNING: There is more than one date. Taking the first one : " + date
        elif len(datelist) == 0:
            print "WARNING: There is no date."
            date = "undefined"
    else:
        finddate = etree.ETXPath("string(//{%s}time[@class=%r]/@datetime)" % (HTMLNS,DATETYPE))
        date = finddate(doc)
    return date

def gettitle(doc):
    """return a list of markup and text being the title of the document"""
    findtitle =  etree.ETXPath("//{%s}h1[text()]" % HTMLNS)
    if len(findtitle(doc)) == 0:
        sys.exit("ERROR: The document has no title")
    title = findtitle(doc)[0]
    titlemarkup = etree.tostring(title)
    titletext = gettext(title)
    return titlemarkup, titletext

# MAIN

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
    print "TITLE: ", gettitle(rawpost)
    print "CREATED: ", getdocdate(rawpost, STATUS, 'created')
    print "MODIFIED", getdocdate(rawpost, STATUS, 'modified')
    
if __name__ == "__main__":
    sys.exit(main())


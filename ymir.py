#!/usr/bin/env python2.7
# encoding: utf-8
"""
ylmir.py

Created by Karl Dubost on 2011-12-03.
Copyright (c) 2011 Grange. All rights reserved.
"""

import sys
import argparse
from lxml.html import tostring, html5parser
from lxml import etree
from lxml.etree import Element, SubElement

# CONFIG 
SITENAME = "Les carnets Web de La Grange"
DOMAIN = "la-grange.net"
SITE = "http://www.%s/" % (DOMAIN)
STATUSLIST = ['draft','pub','acl']
DATETYPELIST = ['created','modified']
LICENSELIST = {'ccby': 'http://creativecommons.org/licenses/by/2.0/fr/', 
               'copy': u'©'}
AUTHOR = "Karl Dubost"
AUTHORURL = "http://www.la-grange.net/karl/"
FEEDIDTAG = "tag:la-grange.net,2000-04-12:karl"
FEEDATOMNOM = "feed.atom"
HTMLNS = "http://www.w3.org/1999/xhtml"
ATOMNS = "http://www.w3.org/2005/Atom"
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

def getdocdate(doc, DATETYPE):
    """return the creation date of the document in ISO format YYYY-MM-DD
    Input the document, typeofdate in between created and modified"""
    # TODO: check if the format is correct aka YYYY-MM-DD
    if DATETYPE not in DATETYPELIST:
        sys.exit("ERROR: No valid type for the date: " + DATETYPE)            
    finddate = etree.ETXPath("string(//{%s}time[@class=%r]/@datetime)" % (HTMLNS,DATETYPE))
    date = finddate(doc)
    return date

def getcontent(doc):
    """return the full content of an article"""
    findcontent = etree.ETXPath("//{%s}article" % HTMLNS)
    content = findcontent(doc)
    return etree.tostring(content[0], method="html",encoding="utf-8")


def gettitle(doc):
    """return a list of markup and text being the title of the document"""
    findtitle =  etree.ETXPath("//{%s}h1[text()]" % HTMLNS)
    if len(findtitle(doc)) == 0:
        sys.exit("ERROR: The document has no title")
    title = findtitle(doc)[0]
    titlemarkup = etree.tostring(title,encoding="utf-8")
    titletext = etree.tostring(title,encoding="utf-8",method="text")
    return titlemarkup, titletext

def makeblogpost(doc):
    """create a blog post ready to be publish from a raw or already published document"""
    pass
    
def makefeedentry(url, tagid, posttitle, created, modified, postcontent):
    """create an individual Atom feed entry from a ready to be publish post"""
    # etree.register_namespace("", ATOMNS)
    entry = Element('entry')
    id = SubElement(entry, 'id')
    id.text = tagid
    linkfeedentry = SubElement(entry, 'link')
    linkfeedentry.attrib["rel"] = "alternate"
    # TODO: This should be probably on a case by case.
    linkfeedentry.attrib["type"] = "text/html"
    linkfeedentry.attrib["href"] = url
    title = SubElement(entry, 'title')
    title.text = posttitle
    published = SubElement(entry, 'published')
    published.text = created
    updated = SubElement(entry, 'updated')
    updated.text = modified
    content = SubElement(entry, 'content')
    content.attrib["type"] = "xhtml"
    divcontent = SubElement(content, 'div')
    divcontent.attrib["xmlns"] = HTMLNS
    divcontent.text = postcontent.decode("utf-8")
    return etree.tostring(entry, pretty_print=True, encoding="utf-8")
    
def createtagid(urlpath,isodate):
    """Create a unide tagid for a given blog post
    tag:la-grange.net,2012-01-24:2012/01/24/silence"""
    tagid = "tag:%s,%s:%s" % (DOMAIN,isodate,urlpath)
    return tagid

def updatefeed(feedentry):
    """Update the feed with the last individual feed entry"""
    pass

def updateannualindex(feedentry):
    """update the HTML Annual index with the feedendry"""
    pass

def updatemonthlyindex(feedentry):
    """update the HTML Monthly index with the feedendry"""
    pass

def updatearchivemap():
    """update the archive map page for new months and/or new years.
    not sure it is necessary. Manually is kind of cool with less 
    dependencies."""
    pass

def createmonthlyindex(month):
    """create a monthly index when it doesn't exist"""
    pass

def createannualindex(year):
    """create an annual index when it doesn't exist"""
    pass

# MAIN

def main():

    # Parsing the cli
    parser = argparse.ArgumentParser(description="Managing Web site blog posts")

    parser.add_argument('rawpost', metavar='FILE', help='file to be processed', action='store', nargs=1, type=argparse.FileType('rt'))
    parser.add_argument('-o', '--output', help='the blog post ready to be sync', nargs=1, dest="output", type=argparse.FileType('wt'))
    atomgroup = parser.add_mutually_exclusive_group()
    atomgroup.add_argument('--atom', help='create an atom feed. DEFAULT', action='store_true', dest="createfeed", default=True)
    atomgroup.add_argument('--noatom', help='do not create the atom feed', action='store_false', dest='createfeed', default=False)

    args = parser.parse_args()
    rawpostpath = args.rawpost[0]

    # Parse the document    
    rawpost = parserawpost(rawpostpath)
    # A few tests when developing 
    STATUS = getdocstatus(rawpost)
    titlemarkup, title = gettitle(rawpost)
    title = title.decode("utf-8")
    print "TITLE: ", title
    print "TITLEMARKUP: ", titlemarkup
    created = getdocdate(rawpost, 'created')
    modified = getdocdate(rawpost, 'modified')
    print "CREATED:  ", created
    print "MODIFIED: ", modified
    content = getcontent(rawpost)
    urlpath = "2010/12/24/foo"
    url= "%s%s" % (SITE,urlpath)
    tagid =  createtagid(urlpath,created)
    print makefeedentry(url, tagid, title, created, modified, content)
    
if __name__ == "__main__":
    sys.exit(main())


#!/usr/bin/env python2.7
# encoding: utf-8
"""
ylmir.py

Created by Karl Dubost on 2011-12-03.
Copyright (c) 2011 Grange. All rights reserved.
"""

import sys, os
import argparse
from lxml.html import tostring, html5parser
from lxml import etree
from lxml.etree import Element, SubElement

# CONFIG SITE
DOMAIN = u"la-grange.net"
SITE = u"http://www.%s/" % (DOMAIN)
FAVICON = SITE + "favicon"


SITENAME = u"Les carnets Web de La Grange"
TAGLINE = u"Rêveries le long d'un brin de chèvrefeuille"

FEEDTAGID = u"tag:la-grange.net,2000-04-12:karl"
FEEDLANG = u"fr"
FEEDATOMNOM = u"feed.atom"
FEEDATOMURL = u"%s%s" % (SITE,FEEDATOMNOM)

STATUSLIST = [u'draft',u'pub',u'acl']
DATETYPELIST = [u'created',u'modified']
LICENSELIST = {u'ccby': u'http://creativecommons.org/licenses/by/2.0/fr/', 
               u'copy': u'©'}

AUTHOR = u"Karl Dubost"
AUTHORURI = u"http://www.la-grange.net/karl/"

HTMLNS = u"http://www.w3.org/1999/xhtml"
ATOMNS = u"http://www.w3.org/2005/Atom"
HTML = "{%s}" % HTMLNS
ATOM = "{%s}" % ATOMNS
NSMAP = {None : HTMLNS}
NSMAP2 = {None : ATOMNS}

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
    #TODO find a way to send the element with only the namespace on the first element.
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
    return content[0]


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

def makefeedskeleton(websitetitle, tagline, feedtagid, lang, feedatomurl, site, license, faviconlink, authorname, authoruri):
    """create the feed skeleton for a specific Web site"""
    feed = Element('feed')
    feed.attrib['lang'] = lang

    # Web site title
    title = SubElement(feed, 'title')
    title.text = websitetitle
    
    # Tagline
    subtitle = SubElement(feed, 'subtitle')
    subtitle.text = tagline

    # feedid
    feedid = SubElement(feed, 'id')
    feedid.text = feedtagid    

    # updated 
    updated = SubElement(feed, 'updated')

    # link self atom
    linkselfatom = SubElement(feed, 'link')
    linkselfatom.attrib["rel"] = "self"
    linkselfatom.attrib["type"] = "application/atom+xml"
    linkselfatom.attrib["href"] = FEEDATOMURL

    # link alternate blog
    linkselfatom = SubElement(feed, 'link')
    linkselfatom.attrib["rel"] = "alternate"
    linkselfatom.attrib["type"] = "application/xhtml+xml"
    linkselfatom.attrib["href"] = site

    # link license
    linkselfatom = SubElement(feed, 'link')
    linkselfatom.attrib["rel"] = "license"
    linkselfatom.attrib["href"] = license

    # icon
    icon = SubElement(feed, 'icon')
    icon.text = faviconlink
    
    # author
    author = SubElement(feed, 'author')
    name = SubElement(author, 'name')
    name.text = authorname
    # email = SubElement(author, 'email')
    # email.text = FEEDEMAIL
    uri = SubElement(author, 'uri')
    uri.text = authoruri
    
    return feed
    
    
def makefeedentry(url, tagid, posttitle, created, modified, postcontent):
    """create an individual Atom feed entry from a ready to be publish post"""
    entry = Element('entry',nsmap=NSMAP2)
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
    # changing the namespace to HTML 
    # so only the local root element (div) will get the namespace
    divcontent = SubElement(content, "{%s}div"%HTMLNS, nsmap=NSMAP)
    # Adding a full tree fragment.
    divcontent.append(postcontent)
    linkselfatom = SubElement(entry, 'link',nsmap=NSMAP2)
    linkselfatom.attrib["rel"] = "license"
    linkselfatom.attrib["href"] = LICENSELIST['ccby']
    return entry
    
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

def updatemonthlyindex(indexmarkup, monthindexpath):
    """update the HTML Annual index with the feedendry"""
    # is there a monthly index.
    if os.path.isfile(monthindexpath):
        monthlyindex = parserawpost(monthindexpath)
    else:
        # TODO
        print "need to create index file"
        createmonthlyindex(monthindexpath)

def createindexmarkup(postpath, created, modified, title):
    """Create the Markup necessary to update the indexes"""
    dcreated = {'class':'created', 'datetime':created}
    dmodified = {'class':'modified', 'datetime':modified}
    # Creating the Markup
    li = etree.Element('li')
    ctime = etree.SubElement(li,'time', dcreated)
    ctime.text = created
    ctime.tail = u" "
    mtime = etree.SubElement(li,'time', dmodified)
    mtime.text = modified
    mtime.tail = u": "
    anchor = etree.SubElement(li, 'a', {'href':postpath})
    anchor.text = title.strip()
    return li

def updatearchivemap():
    """update the archive map page for new months and/or new years.
    not sure it is necessary. Manually is kind of cool with less 
    dependencies."""
    pass

def createmonthlyindex(monthindexpath):
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
    abspathpost = os.path.abspath(rawpostpath.name)
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

    # What are the paths?
    monthabspath = os.path.dirname(os.path.dirname(abspathpost))
    yearabspath = os.path.dirname(monthabspath)
    rootabspath = os.path.dirname(yearabspath)
    postpath = abspathpost[len(rootabspath):]
    monthindexpath = monthabspath+"/index.html"
    tagid =  createtagid(abspathpost,created)
    feedentry = makefeedentry(abspathpost, tagid, title, created, modified, content)
    indexmarkup = createindexmarkup(postpath[:-5], created, modified, title)
    updatemonthlyindex(indexmarkup, monthindexpath)

    # feedbase = makefeedskeleton(SITENAME, TAGLINE, FEEDTAGID, FEEDLANG, FEEDATOMURL, SITE, LICENSELIST['ccby'], FAVICON, AUTHOR, AUTHORURI)
    # print etree.tostring(monthlyindex, encoding="utf-8",pretty_print=True)
    # two cases 
    # either it is already in the list: update
    # It is not in the list: new post
    # check the path
    
if __name__ == "__main__":
    sys.exit(main())


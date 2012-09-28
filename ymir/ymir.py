#!/usr/bin/env python2.7
# encoding: utf-8
"""
ymir.py

Created by Karl Dubost on 2011-12-03.
Copyright (c) 2011 Grange. All rights reserved.
see LICENSE.TXT
"""

import sys
import os
import locale
from time import gmtime, strftime, localtime
import argparse
from lxml.html import html5parser
from lxml import etree
from lxml.etree import Element, SubElement
from string import Template
from ConfigParser import SafeConfigParser
import logging

# CONFIG SITE
DOMAIN = u"la-grange.net"
SITE = u"http://www.%s/" % (DOMAIN)
FAVICON = SITE + "favicon"
CODEPATH = os.path.dirname(sys.argv[0])
TEMPLATEDIR = CODEPATH + "/../templates/"

SITENAME = u"Les carnets Web de La Grange"
TAGLINE = u"Rêveries le long d'un brin de chèvrefeuille"

FEEDTAGID = u"tag:la-grange.net,2000-04-12:karl"
FEEDLANG = u"fr"
FEEDATOMNOM = u"feed.atom"
FEEDATOMURL = u"%s%s" % (SITE, FEEDATOMNOM)

STATUSLIST = [u'draft', u'pub', u'acl']
DATETYPELIST = [u'created', u'modified']
LICENSELIST = {u'ccby': u'http://creativecommons.org/licenses/by/2.0/fr/', u'copy': u'©'}

AUTHOR = u"Karl Dubost"
AUTHORURI = u"http://www.la-grange.net/karl/"

HTMLNS = u"http://www.w3.org/1999/xhtml"
ATOMNS = u"http://www.w3.org/2005/Atom"
HTML = "{%s}" % HTMLNS
ATOM = "{%s}" % ATOMNS
NSMAP = {None: HTMLNS}
NSMAP2 = {None: ATOMNS}
NSMAP3 = {'html': HTMLNS}

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


def getdocdate(doc, DATETYPE):
    """return the creation date of the document in ISO format YYYY-MM-DD
    Input the document, typeofdate in between created and modified"""
    # TODO: check if the format is correct aka YYYY-MM-DD
    if DATETYPE not in DATETYPELIST:
        sys.exit("ERROR: No valid type for the date: " + DATETYPE)
    finddate = etree.ETXPath("string(//{%s}time[@class=%r]/@datetime)" % (HTMLNS, DATETYPE))
    date = finddate(doc)
    return date


def getcontent(doc):
    """return the full content of an article"""
    findcontent = etree.ETXPath("//{%s}article" % HTMLNS)
    content = findcontent(doc)[0]
    # we want the content without the dates and the title
    findheader = etree.ETXPath("//{%s}header" % HTMLNS)
    header = findheader(content)[0]
    content.remove(header)
    return content


def gettitle(doc):
    """return a list of markup and text being the title of the document"""
    findtitle = etree.ETXPath("//{%s}h1[text()]" % HTMLNS)
    if not findtitle(doc):
        sys.exit("ERROR: The document has no title")
    title = findtitle(doc)[0]
    titlemarkup = etree.tostring(title, encoding="utf-8")
    titletext = etree.tostring(title, encoding="utf-8", method="text")
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
    entry = Element('entry', nsmap=NSMAP2)
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
    divcontent = SubElement(content, "{%s}div" % HTMLNS, nsmap=NSMAP)
    # Adding a full tree fragment.
    divcontent.append(postcontent)
    linkselfatom = SubElement(entry, 'link', nsmap=NSMAP2)
    linkselfatom.attrib["rel"] = "license"
    linkselfatom.attrib["href"] = LICENSELIST['ccby']
    return entry


def createtagid(urlpath, isodate):
    """Create a unide tagid for a given blog post
    tag:la-grange.net,2012-01-24:2012/01/24/silence"""
    tagid = "tag:%s,%s:%s" % (DOMAIN, isodate[0:10], urlpath.lstrip(SITE))
    return tagid


def nowdate(format=""):
    """Compute date in different formats I need"""
    # date in French please
    my_locale = "fr_FR"
    locale.setlocale(locale.LC_ALL, my_locale)
    if format == "rfc3339":
        return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    elif format == "iso":
        return strftime("%Y-%m-%d", gmtime())
    elif format == "path":
        return strftime("%Y/%m/%d", gmtime())
    elif format == "humain":
        # remove the leading 0 of the date
        dategeek = strftime("%d %B %Y", gmtime())
        if dategeek.startswith('0'):
            dategeek = dategeek.lstrip('0')
        return dategeek
    elif format == "humainlong":
        # Remove the leading 0
        # And add the day of the week
        # "Vendredi "+ "3 février 2012"
        dategeek = strftime("%d %B %Y", localtime())
        if dategeek.startswith('0'):
            dategeek = dategeek.lstrip('0')
        return strftime("%A ", localtime()) + dategeek
    else:
        print "wrong format"
        sys.exit(1)


def updatefeed(feedentry):
    """Update the feed with the last individual feed entry"""
    pass


def updateannualindex(feedentry):
    """update the HTML Annual index with the feedendry"""
    pass


def updatemonthlyindex(indexmarkup, monthindexpath):
    """update the HTML Annual index with the feedendry"""
    print etree.tostring(indexmarkup, encoding="utf-8")
    # is there a monthly index.
    if os.path.isfile(monthindexpath):
        monthlyindex = parserawpost(monthindexpath)
    else:
        # TODO
        print "need to create index file"
        createmonthlyindex(monthindexpath)
    # grab the path and the modified date for the blog post
    anchor = indexmarkup.xpath("/li/a")
    newmodified = indexmarkup.xpath("/html:li/time[@class='modified']/text()", namespaces={'html': 'http://www.w3.org/1999/xhtml'})[0]
    link = anchor[0].get('href')
    # check if the element is already in the list
    findli = etree.ETXPath("//{%s}li/{%s}a" % (HTMLNS, HTMLNS))
    fulllist = findli(monthlyindex)
    ENDLIST = True
    for item in fulllist:
        # if yes replace it with the new one.
        if item.get('href') == link:
            ENDLIST = False
            for timeelt in item.itersiblings(preceding=True):
                if timeelt.get('class') == 'modified':
                    timeelt.set('datetime', newmodified)
                    timeelt.text = newmodified
            return etree.tostring(monthlyindex, encoding="utf-8")

    if ENDLIST:
        findul = etree.ETXPath("//{%s}ul" % HTMLNS)
        ul = findul(monthlyindex)[0]
        print ul
        ul.append(indexmarkup)
        print "Add markup at the end"
        return etree.tostring(monthlyindex, encoding="utf-8")

    # if NO add it to the end of the list?
    # hmmm what about if the date is not in order :)


# NEED TO FIX THE NAMESPACE output.
def createindexmarkup(postpath, created, title):
    """Create the Markup necessary to update the indexes"""
    dcreated = {'class': 'created', 'datetime': created}
    # Creating the Markup
    li = etree.Element("{%s}li" % HTMLNS, nsmap=NSMAP)
    ctime = etree.SubElement(li, 'time', dcreated)
    ctime.text = created[:10]
    ctime.tail = u" : "
    anchor = etree.SubElement(li, 'a', {'href': postpath})
    anchor.text = title.strip()
    return li


def updatearchivemap():
    """update the archive map page for new months and/or new years.
    not sure it is necessary. Manually is kind of cool with less
    dependencies."""
    pass


def createmonthlyindex(indexmarkup):
    """create a monthly index when it doesn't exist"""
    # Code ici pour lire un fichier avec des variables
    # substituer les variables par les valeurs du mois
    # sauver le fichier au bon endroit
    print "Do not forget to update /map with your tiny hands"
    with open(TEMPLATEDIR + 'index-mois.html', 'r') as source:
        t = Template(source.read())
        datestring = nowdate('iso')
        datehumain = nowdate('humain')
        # to get month, we split in 3 the human date and take the second argument
        datemois = datehumain.split(' ')[1]
        indexli = etree.tostring(indexmarkup, pretty_print=True, encoding='utf-8')
        result = t.substitute(isodateshort = datestring, monthname = datemois, year = datestring[:4], humandate = datehumain, firstentry = indexli)
        # need to write it on the filesystem.
        print result


def createannualindex(year):
    """create an annual index when it doesn't exist"""
    pass

# MAIN


def main():
    logging.basicConfig(filename='log-ymir.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    # Parsing the cli
    parser = argparse.ArgumentParser(description="Managing Web site blog posts")

    parser.add_argument('rawpost', metavar='FILE', help='file to be processed', action='store', nargs=1, type=argparse.FileType('rt'))
    parser.add_argument('-o', '--output', help='the blog post ready to be sync', nargs=1, dest="output", type=argparse.FileType('wt'))
    atomgroup = parser.add_mutually_exclusive_group()
    atomgroup.add_argument('--atom', help='create an atom feed. DEFAULT', action='store_true', dest="createfeed", default=True)
    atomgroup.add_argument('--noatom', help='do not create the atom feed', action='store_false', dest='createfeed', default=False)

    args = parser.parse_args()

    # Reading the Blog Config file
    # Preparing the future of reading values from a config file.
    blogcfg = SafeConfigParser()
    blogcfg.read(CODEPATH + '/blog.cfg')
    #print "CONFIG: ", blogcfg.get('blog', 'sitename')

    # Parse the document
    rawpostpath = args.rawpost[0]
    rawpost = parserawpost(rawpostpath)
    abspathpost = os.path.abspath(rawpostpath.name)
    # A few tests when developing
    titlemarkup, title = gettitle(rawpost)
    title = title.decode("utf-8").strip()
    logging.info("TITLE: %s" % (title))
    created = getdocdate(rawpost, 'created')
    logging.info("CREATED: %s" % (created))
    modified = getdocdate(rawpost, 'modified')
    logging.info("MODIFIED: %s" % (modified))
    content = getcontent(rawpost)

    # What are the paths?
    monthabspath = os.path.dirname(os.path.dirname(abspathpost))
    yearabspath = os.path.dirname(monthabspath)
    rootabspath = os.path.dirname(yearabspath)
    postpath = abspathpost[len(rootabspath):]
    posturl = "%s%s" % (SITE[:-1], postpath[:-5])
    monthindexpath = monthabspath + "/index.html"
    # Create Markup for the monthly and yearly index file
    indexmarkup = createindexmarkup(postpath[:-5], created, title)
    print etree.tostring(indexmarkup, pretty_print=True, encoding='utf-8')
    # Create the monthly index if it doesn't exist yet
    # Happen once a month
    if not os.path.isfile(monthindexpath):
        createmonthlyindex(indexmarkup)
    # Create the yearly index if it doesn't exist yet
    # Happen once a year
    # TODO
    # Create Feed
    tagid = createtagid(posturl, created)
    feedentry = makefeedentry(posturl, tagid, title, created, nowdate('rfc3339'), content)
    print etree.tostring(feedentry, pretty_print=True, encoding='utf-8')
    # print updatemonthlyindex(indexmarkup, monthindexpath)

    # feedbase = makefeedskeleton(SITENAME, TAGLINE, FEEDTAGID, FEEDLANG, FEEDATOMURL, SITE, LICENSELIST['ccby'], FAVICON, AUTHOR, AUTHORURI)
    # print etree.tostring(monthlyindex, encoding="utf-8",pretty_print=True)
    # two cases
    # either it is already in the list: update
    # It is not in the list: new post
    # check the path

if __name__ == "__main__":
    sys.exit(main())
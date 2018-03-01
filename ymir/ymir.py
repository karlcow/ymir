#!/usr/bin/env python2.7
# encoding: utf-8
"""
Code for managing la-grange.net.

Created by Karl Dubost on 2011-12-03.
Copyright (c) 2011 Grange. All rights reserved.
see LICENSE.TXT
"""

import argparse
import ConfigParser
import datetime
import logging
import os
import shutil
import string
from StringIO import StringIO
import sys

from lxml import etree
from lxml.etree import Element
from lxml.etree import SubElement
import lxml.html
from lxml.html import html5parser

from utils import helper
from utils import parsing

# from tracer import show_guts

# CONFIG SITE
config = ConfigParser.ConfigParser()
config.read('blog.cfg')

DOMAIN = u"la-grange.net"
SITE = u"http://www.%s/" % (DOMAIN)
ROOT_TOKEN = u'tagid-2000-04-12'
FAVICON = SITE + "favicon"
CODEPATH = os.path.dirname(sys.argv[0])
TEMPLATEDIR = CODEPATH + "/../templates/"

SITENAME = u"Les carnets Web de La Grange"
TAGLINE = u"Rêveries le long d'un brin de chèvrefeuille"

FEEDTAGID = u"tag:la-grange.net,2000-04-12:karl"
FEEDLANG = u"fr"
FEEDATOMNOM = u"feed.atom"
FEEDATOMURL = u"%s%s" % (SITE, FEEDATOMNOM)
FEED_MAX_POSTS = 25

STATUSLIST = [u'draft', u'pub', u'acl']
DATETYPELIST = [u'created', u'modified']
LICENSELIST = {u'ccby': u'http://creativecommons.org/licenses/by/2.0/fr/',
               u'copy': u'©'}

AUTHOR = u"Karl Dubost"
AUTHORURI = u"http://www.la-grange.net/karl/"

HTMLNS = u"http://www.w3.org/1999/xhtml"
ATOMNS = u"http://www.w3.org/2005/Atom"
HTML = "{%s}" % HTMLNS
ATOM = "{%s}" % ATOMNS
NSMAP = {None: HTMLNS}
NSMAP2 = {None: ATOMNS}
NSMAP3 = {'html': HTMLNS}
NSMAP4 = {'atom': ATOMNS}

# CONFIG with cli
STYLESHEET = "/2011/12/01/proto/style/article.css"
STATUS = ""
MAXFEEDITEM = 20
LICENSE = "ccby"

DATENOW = datetime.datetime.today()

# PATHS

help_message = """
This script has been entirely created
for processing text files for the site
La Grange http://www.la-grange.net/.
"""


def parserawpost(rawpostpath):
    """Given a path, parse an html file."""
    doc = html5parser.parse(rawpostpath).getroot()
    logging.info("parserrawpost: HTML document parsed")
    return doc


def parse_feed(feed_path):
    """Given the feed path, return a <type 'lxml.etree._Element'>."""
    parser = etree.XMLParser(ns_clean=True)
    with open(feed_path, 'r') as source:
        feed_tree = etree.parse(source, parser)
    logging.info("parse_feed: Feed has been parsed")
    return feed_tree


def find_root(directory, token):
    """Find the root of a directory tree based on a token."""
    # Make sure we have a full path instead of a relative path
    if directory.startswith('.'):
        directory = os.path.realpath(directory)
    # Create a list of the files in the current directory
    # If it fails the path doesn't exist
    try:
        files_only = [f for f in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory, f))]
    except Exception:
        return None
    # Check if the token is not among the files
    if token not in files_only:
        # if '/', we are at the filesystem root
        if directory == '/':
            return None
        # Recursion with the upper directory
        newpath = os.path.realpath(directory + '/../')
        directory = find_root(newpath, token)
    logging.info('find_root: The root is %s' % (directory))
    return directory


def getdocdate(doc, DATETYPE):
    """Return the creation date of the document in ISO format YYYY-MM-DD.

    Input the document, typeofdate in between created and modified.
    """
    if DATETYPE not in DATETYPELIST:
        sys.exit("ERROR: No valid type for the date: " + DATETYPE)
    finddate = etree.ETXPath(
        "string(//{%s}time[@class=%r]/@datetime)" % (HTMLNS, DATETYPE))
    date = finddate(doc)
    return date


def getcontent(doc):
    """Return the full content of an article."""
    findcontent = etree.ETXPath("//{%s}article" % HTMLNS)
    content = findcontent(doc)[0]
    # we want the content without the dates and the title
    findheader = etree.ETXPath("//{%s}header" % HTMLNS)
    header = findheader(content)[0]
    content.remove(header)
    return content


def makefeedentry(feedentry_data):
    """Create an individual Atom feed entry from a ready to be publish post."""
    entry = Element('{http://www.w3.org/2005/Atom}entry', nsmap=NSMAP2)
    id_element = SubElement(entry, 'id')
    id_element.text = feedentry_data['tagid']
    linkfeedentry = SubElement(entry, 'link')
    linkfeedentry.attrib["rel"] = "alternate"
    linkfeedentry.attrib["type"] = "text/html"
    linkfeedentry.attrib["href"] = feedentry_data['url']
    title = SubElement(entry, 'title')
    title.text = feedentry_data['title']
    published = SubElement(entry, 'published')
    published.text = feedentry_data['created']
    updated = SubElement(entry, 'updated')
    updated.text = feedentry_data['modified']
    content = SubElement(entry, 'content')
    content.attrib["type"] = "xhtml"
    # changing the namespace to HTML
    # so only the local root element (div) will get the namespace
    divcontent = SubElement(content, "{%s}div" % HTMLNS, nsmap=NSMAP)
    # Adding a full tree fragment.
    divcontent.append(feedentry_data['content'])
    linkselfatom = SubElement(entry, 'link', nsmap=NSMAP2)
    linkselfatom.attrib["rel"] = "license"
    linkselfatom.attrib["href"] = LICENSELIST['ccby']
    entry = etree.parse(StringIO(etree.tostring(entry, encoding='utf-8')))
    logging.info("makefeedentry: new entry created")
    return entry


def createtagid(urlpath, isodate):
    """Create a unide tagid for a given blog post.

    Example: tag:la-grange.net,2012-01-24:2012/01/24/silence
    """
    tagid = "tag:%s,%s:%s" % (DOMAIN, isodate[0:10], urlpath.lstrip(SITE))
    return tagid


def rfc3339_to_datetime(rfc3339_date_time):
    """Convert dates.

    Incomplete because I know my format.
    Do not reuse elsewhere.
    2014-04-04T23:59:00+09:00
    2014-04-04T23:59:00Z
    """
    # Extraire la date et le temps sans le fuseau
    # 2014-04-04T23:59:00+09:00 -> 2014-04-04T23:59:00
    date_time, offset = rfc3339_date_time[:19], rfc3339_date_time[19:]
    # convertir en objet datetime
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
    # extraire le fuseau horaire
    # 2014-04-04T23:59:00+09:00 -> +09:00
    # 2014-04-04T23:59:00Z      -> Z
    # Si Z, on est déjà en UTC.
    if 'Z' not in offset:
        tz_hours, tz_minutes = int(offset[1:3]), int(offset[4:6])
        if '+' in offset:
            # si + on doit déduire le temps pour obtenir l'heure en UTC
            date_time -= datetime.timedelta(hours=tz_hours, minutes=tz_minutes)
        else:
            # si - on doit ajouter le temps pour obtenir l'heure en UTC
            date_time += datetime.timedelta(hours=tz_hours, minutes=tz_minutes)
    return date_time


def update_feed(feedentry, feed_path):
    """Update the feed with the last individual feed entry.

    * return None if nothing has changed
    * add a new entry, delete the last if a new post
    * add a new entry, remove the old entry if post has changed.
    """
    NEW_ENTRY = False
    feed = parse_feed(feed_path)
    # XPath for finding tagid
    find_entry = etree.ETXPath("//{%s}entry" % ATOMNS)
    find_id = etree.ETXPath("{%s}id/text()" % ATOMNS)
    find_date = etree.ETXPath("{%s}updated/text()" % ATOMNS)
    # We need the information about the new entry
    new_id = find_id(feedentry)[0]
    new_updated = find_date(feedentry)[0]
    # Processing and comparing
    entries = find_entry(feed)
    posts_number = len(entries)
    for entry in entries:
        old_id = find_id(entry)[0]
        old_updated = find_date(entry)[0]
        if old_id == new_id:
            if old_updated == new_updated:
                logging.info("The feed has not changed.")
                return None
            else:
                logging.info("The feed has been updated.")
                # we remove from feed the specific entry
                entry.getparent().remove(entry)
                # Find the first entry element in the feed
                position = feed.getroot().index(
                    feed.find("//{%s}entry" % ATOMNS))
                feed.getroot().insert(position, feedentry.getroot())
                # Change the <updated> date of the feed
                feed.find("//{%s}updated" % ATOMNS).text = new_updated
                return lxml.html.tostring(feed, encoding='utf-8')
    else:
        logging.info("This is a new feed entry.")
        NEW_ENTRY = True
    if NEW_ENTRY:
        if posts_number > FEED_MAX_POSTS:
            entries[-1].getparent().remove(entries[-1])
        position = feed.getroot().index(feed.find("//{%s}entry" % ATOMNS))
        feed.getroot().insert(position, feedentry.getroot())
        # Change the <updated> date of the feed
        feed.find("//{%s}updated" % ATOMNS).text = new_updated
        return lxml.html.tostring(feed, encoding='utf-8')
    return None


def update_home_index(feed_path, home_path, id_name):
    """Update the HTML index with the feedendry content."""
    # Get HTML from the index
    if os.path.isfile(home_path):
        html = lxml.html.parse(home_path)
        home = html.getroot()
    else:
        logging.error("WRONG PATH: %s" % (home_path))
    # Get an entry dictionary from the Feed
    entries = last_posts(feed_path)
    # Generate string with markup
    home_template = """<ul id="{id}">
    {posts_list}
    </ul>
    """
    posts_list = last_posts_html(entries)
    home_index = home_template.format(
        id=id_name,
        posts_list=posts_list)
    lis = lxml.html.fragment_fromstring(home_index.decode('utf-8'))
    # replace the content of the home index
    blog_ul = home.get_element_by_id(id_name)
    blog_ul.getparent().replace(blog_ul, lis)
    return lxml.html.tostring(html, encoding='utf-8')


def updatemonthlyindex(indexmarkup, monthindexpath):
    """Update the HTML Annual index with the feedendry."""
    # print etree.tostring(indexmarkup, encoding="utf-8")
    # is there a monthly index.
    if os.path.isfile(monthindexpath):
        monthlyindex = lxml.html.parse(monthindexpath).getroot()
        logging.info("Monthly Index exists")
    else:
        logging.warn("Monthly index doesn’t exist. TOFIX")
        createmonthlyindex(monthindexpath)
    # grab the list of entry
    findentrylist = etree.ETXPath("//section[@id='month-index']/ul/li")
    entries = findentrylist(monthlyindex)
    find_href = etree.ETXPath("a/@href")
    find_created = etree.ETXPath("time/@datetime")
    # find_title = etree.ETXPath("a/text()")
    href_ref = find_href(indexmarkup)[0]
    created_ref = find_created(indexmarkup)[0]
    # title_ref = find_title(indexmarkup)[0]

    for entry in entries:
        href_entry = find_href(entry)[0]
        created_entry = find_created(entry)[0]
        print("ENTRY: ", created_entry, " TO ", created_ref)
        if href_entry == href_ref:
            print('same uri', href_entry)
            # we check the date
            # we check the title
            # if changed replace
        else:
            pass


def createindexmarkup(postpath, created, title):
    """Create the Markup necessary to update the indexes."""
    dcreated = {'class': 'created', 'datetime': created}
    # Creating the Markup
    # li = etree.Element("{%s}li" % HTMLNS, nsmap=NSMAP)
    li = etree.Element("li")
    ctime = etree.SubElement(li, 'time', dcreated)
    ctime.text = created[:10]
    ctime.tail = u" : "
    anchor = etree.SubElement(li, 'a', {'href': postpath})
    anchor.text = title.strip()
    return li


# def updatearchivemap():
#     """Update the archive map page for new months and/or new years.

#     not sure it is necessary. Manually is kind of cool with less
#     dependencies.
#     """
#     pass


def createmonthlyindex(indexmarkup, monthindexpath):
    """Create a monthly index when it doesn't exist."""
    # Code ici pour lire un fichier avec des variables
    # substituer les variables par les valeurs du mois
    # sauver le fichier au bon endroit
    msg = "Do not forget to update /map with your tiny hands"
    logging.info("%s" % (msg))

    with open(TEMPLATEDIR + 'index-mois.html', 'r') as source:
        t = string.Template(source.read())
        datestring = helper.nowdate(DATENOW, 'iso')
        datehumain = helper.nowdate(DATENOW, 'humain')
        # to get month, we split in 3 the human date and take the second
        # argument
        datemois = datehumain.split(' ')[1]
        indexli = etree.tostring(
            indexmarkup, pretty_print=True, encoding='utf-8')
        result = t.substitute(isodateshort=datestring,
                              monthname=datemois,
                              year=datestring[:4],
                              humandate=datehumain,
                              firstentry=indexli)
        # need to write it on the filesystem.
    with open(monthindexpath, 'w') as monthindex:
        monthindex.write(result)


def last_posts(feed_path):
    """Create a dictionary index of the last post using the Atom feed."""
    entries = []
    feed_root = parse_feed(feed_path)
    # Information we need: title, dates, link
    find_entry = etree.ETXPath("//{%s}entry" % ATOMNS)
    find_title = etree.ETXPath("{%s}title/text()" % ATOMNS)
    find_published = etree.ETXPath("{%s}published/text()" % ATOMNS)
    find_updated = etree.ETXPath("{%s}updated/text()" % ATOMNS)
    # Only the link pointing to the blog post
    find_url = etree.ETXPath("{%s}link[@rel='alternate']/@href" % ATOMNS)
    # Extract all the entries
    feed_entries = find_entry(feed_root)
    # We iterate through them
    for entry in feed_entries:
        entry_data = {'title': find_title(entry)[0],
                      'published': find_published(entry)[0],
                      'updated': find_updated(entry)[0],
                      'url': find_url(entry)[0]}
        entries.append(entry_data)
    return entries


def last_posts_html(entries):
    """Return the HTML markup for the last entries."""
    # msg = "Generating HTML markup for last entries in the feed"
    # logging.info("%s" % (msg))
    last_posts_markup = ''
    with open(TEMPLATEDIR + 'last_posts.html', 'r') as source:
        t = string.Template(source.read())
        for entry in entries:
            published = entry['published']
            tshortdate = published[:10]
            last_posts_markup += t.substitute(
                ttitle=entry['title'].encode('utf-8'),
                turl=entry['url'],
                tpublished=published,
                tshortdate=tshortdate)
    return last_posts_markup

# MAIN


def main():
    """Run the core task for processing a file for La Grange."""
    # Logging File Configuration
    logging.basicConfig(filename='log-ymir.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('-'*80)
    # Command Line Interface
    parser = argparse.ArgumentParser(
        description="Managing Web site blog posts")
    parser.add_argument('rawpost', metavar='FILE', help='file to be processed',
                        action='store', nargs=1, type=argparse.FileType('rt'))
    parser.add_argument('-t', '--testmode', action='store_true',
                        help='Run ymir without writing files.')
    args = parser.parse_args()
    # Mode for testing the code without destroying the files
    dryrun = False
    if args.testmode:
        dryrun = True
    # Arguments attribution
    rawpostpath = args.rawpost[0]
    # PATH CONFIGURATIONS
    # Getting the path of the current post on the OS
    abspathpost = os.path.abspath(rawpostpath.name)
    post_directory = os.path.dirname(abspathpost)
    # Finding the root of the Web site
    site_root = find_root(post_directory, ROOT_TOKEN)
    # Post path and full URL without ".html"
    postpath = abspathpost[len(site_root):]
    posturl = "%s%s" % (SITE[:-1], postpath[:-5])
    # Feed
    feed_path = '%s/%s' % (site_root, FEEDATOMNOM)
    # Site Home Page
    home_path = '%s/%s' % (site_root, 'index.html')
    # Monthly index
    monthabspath = os.path.dirname(os.path.dirname(abspathpost))
    monthindexpath = monthabspath + "/index.html"
    # BACKUPS?
    # preparing places for backup
    BACKUP_PATH = '/tmp/lagrange'
    if not os.path.isdir(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)
    feed_path_bkp = '%s/%s' % (BACKUP_PATH, FEEDATOMNOM)
    shutil.copy(feed_path, feed_path_bkp)
    # PROCESSING
    # Parse the document
    rawpost = parserawpost(rawpostpath)
    # Extracting Post Information
    title = parsing.get_title(rawpost)
    title = title.decode("utf-8").strip()
    logging.info("TITLE: %s" % (title))
    created = getdocdate(rawpost, 'created')
    logging.info("CREATED: %s" % (created))
    modified = getdocdate(rawpost, 'modified')
    DATENOW = rfc3339_to_datetime(modified)
    logging.info("MODIFIED: %s" % (modified))
    content = getcontent(rawpost)

    # INDEX MARKUP
    indexmarkup = createindexmarkup(postpath[:-5], created, title)
    # Create the monthly index if it doesn't exist yet
    # Happen once a month
    if not os.path.isfile(monthindexpath):
        createmonthlyindex(indexmarkup, monthindexpath)
    else:
        # TOFIX: updating the monthly index
        # updatemonthlyindex(indexmarkup, monthindexpath)
        print(etree.tostring(indexmarkup, pretty_print=True, encoding='utf-8'))

    # FEED ENTRY MARKUP
    tagid = createtagid(posturl, created)
    # UPDATING FEED
    feedentry_data = {'url': posturl,
                      'tagid': tagid,
                      'title': title,
                      'created': created,
                      'modified': helper.nowdate(DATENOW, 'rfc3339'),
                      'content': content}
    feedentry = makefeedentry(feedentry_data)
    feed_content = update_feed(feedentry, feed_path_bkp)
    if feed_content:
        if not dryrun:
            with open(feed_path, 'w') as feedbkp:
                feedbkp.write(feed_content)
        else:
            print('TESTING: feedbkp.write(feed_content)')
    # UPDATING HOME PAGE
    home_content = update_home_index(feed_path, home_path, 'posts_list')
    if not dryrun:
        with open(home_path, 'w') as home:
            home.write(home_content)
    else:
        print('TESTING: home.write(home_content)')
    # UPDATING MONTHLY INDEX
    # updatemonthlyindex(indexmarkup, monthindexpath)

if __name__ == "__main__":
    sys.exit(main())

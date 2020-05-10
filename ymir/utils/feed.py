#!/usr/bin/env python
# encoding: utf-8
"""Helpers for the code.

Created by Karl Dubost on 2014-12-01.
Copyright (c) 2014 Grange. All rights reserved.
see LICENSE.TXT
"""
from io import StringIO
import logging
import os
import sys

from lxml import etree
from lxml.etree import Element
from lxml.etree import SubElement
import lxml.html

from ymir.utils import helper

HTMLNS = "http://www.w3.org/1999/xhtml"
HTML = "{%s}" % HTMLNS
NSMAP = {None: HTMLNS}
NSMAP3 = {'html': HTMLNS}

ATOMNS = "http://www.w3.org/2005/Atom"
NSMAP2 = {None: ATOMNS}
ATOM = "{%s}" % ATOMNS
NSMAP4 = {'atom': ATOMNS}

LICENSELIST = {'ccby': 'http://creativecommons.org/licenses/by/2.0/fr/',
               'copy': '©'}

DOMAIN = "la-grange.net"
SITE = "http://www.%s/" % (DOMAIN)
ROOT_TOKEN = 'tagid-2000-04-12'
FAVICON = SITE + "favicon"
CODEPATH = os.path.dirname(sys.argv[0])
TEMPLATEDIR = CODEPATH + "/../templates/"

SITENAME = "Les carnets Web de La Grange"
TAGLINE = "Rêveries le long d'un brin de chèvrefeuille"

FEEDTAGID = "tag:la-grange.net,2000-04-12:karl"
FEEDLANG = "fr"
FEEDATOMNOM = "feed.atom"
FEEDATOMURL = "%s%s" % (SITE, FEEDATOMNOM)
FEED_MAX_POSTS = 25

STATUSLIST = ['draft', 'pub', 'acl']
DATETYPELIST = ['created', 'modified']
LICENSELIST = {'ccby': 'http://creativecommons.org/licenses/by/2.0/fr/',
               'copy': '©'}

AUTHOR = "Karl Dubost"
AUTHORURI = "http://www.la-grange.net/karl/"

HTMLNS = "http://www.w3.org/1999/xhtml"
HTML = "{%s}" % HTMLNS
NSMAP = {None: HTMLNS}
NSMAP3 = {'html': HTMLNS}


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
    entry_string = etree.tostring(entry, encoding='unicode')
    # Change the image links to absolute links
    # This will break one day. This is for Anthony Ricaud.
    normalized_entry = entry_string.replace(
        '<img src="/', '<img src="http://www.la-grange.net/')
    # Convert as an elementTree
    entry = etree.parse(StringIO(normalized_entry))
    logging.info("makefeedentry: new entry created")
    return entry


def update_feed(feedentry, feed_path):
    """Update the feed with the last individual feed entry.

    * return None if nothing has changed
    * add a new entry, delete the last if a new post
    * add a new entry, remove the old entry if post has changed.
    """
    new_entry = False
    feed = helper.parse_feed(feed_path)
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
        new_entry = True
    if new_entry:
        if posts_number > FEED_MAX_POSTS:
            entries[-1].getparent().remove(entries[-1])
        position = feed.getroot().index(feed.find("//{%s}entry" % ATOMNS))
        feed.getroot().insert(position, feedentry.getroot())
        # Change the <updated> date of the feed
        feed.find("//{%s}updated" % ATOMNS).text = new_updated
        return lxml.html.tostring(feed, encoding='utf-8')
    return None

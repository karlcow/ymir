#!/usr/bin/env python
# encoding: utf-8
"""
Code for managing la-grange.net.

Created by Karl Dubost on 2011-12-03.
Copyright (c) 2011 Grange. All rights reserved.
see LICENSE.TXT
"""

import argparse
import configparser
from dataclasses import dataclass
import datetime
from io import StringIO
import logging
import os
import shutil
import string
import sys

from lxml import etree
from lxml.etree import Element
from lxml.etree import SubElement
import lxml.html

from ymir.utils import feed
from ymir.utils import helper
from ymir.utils import indexes
from ymir.utils import parsing


# CONFIG SITE
config = configparser.ConfigParser()
config.read('blog.cfg')

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

# CONFIG with cli
STYLESHEET = "/2011/12/01/proto/style/article.css"
STATUS = ""
MAXFEEDITEM = 20
LICENSE = "ccby"

date_now = datetime.datetime.today()

# PATHS

help_message = """
This script has been entirely created
for processing text files for the site
La Grange http://www.la-grange.net/.
"""


@dataclass
class Blog:
    """Blog definition."""
    absolute_root: str
    feed_name: str
    root_token: str
    feed_path: str = ''
    home_index_path: str = ''


@dataclass
class Post:
    """Blog post definition."""
    absolute_path: str
    absolute_site_root: str = ''
    full_content: str = ''
    title: str = ''
    article: str = ''
    created_date: str = ''
    modified_date: str = ''
    web_path: str = ''
    month_index_path: str = ''
    year_index_path: str = ''

    def __post_init__(self):
        self.absolute_site_root = helper.find_root(
            os.path.dirname(self.absolute_path), ROOT_TOKEN)
        self.full_content = helper.parse_raw_post(self.absolute_path)
        self.title = parsing.get_title(self.full_content)
        self.article = parsing.get_content(self.full_content)
        self.created_date = parsing.get_date(self.full_content, 'created')
        self.modified_date = parsing.get_date(self.full_content, 'modified')
        self.web_path = self.absolute_path[len(self.absolute_site_root):]


def createindexmarkup(postpath, created, title):
    """Create the Markup necessary to update the indexes."""
    dcreated = {'class': 'created', 'datetime': created}
    # Creating the Markup
    # li = etree.Element("{%s}li" % HTMLNS, nsmap=NSMAP)
    li = etree.Element("li")
    ctime = etree.SubElement(li, 'time', dcreated)
    ctime.text = created[:10]
    ctime.tail = " : "
    anchor = etree.SubElement(li, 'a', {'href': postpath})
    anchor.text = title.strip()
    return etree.tostring(li, encoding='unicode')


def last_posts(feed_path):
    """Create a list of dictionaries of the last posts using the Atom feed."""
    entries = []
    feed_root = helper.parse_feed(feed_path)
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


def main():
    """Run the core task for processing a file for La Grange."""
    # Logging File Configuration
    logging.basicConfig(filename='log-ymir.txt', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('-' * 80)
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
    raw_post_path = args.rawpost[0]

    # *** PATH CONFIGURATIONS ***
    # Getting the path of the current post on the OS
    abspathpost = os.path.abspath(raw_post_path.name)

    # Finding the root of the Web site
    site_root = helper.find_root(os.path.dirname(abspathpost), ROOT_TOKEN)
    logging.info('site root: {root}'.format(root=site_root))

    # Post path and full URL without ".html"
    postpath = abspathpost[len(site_root):]
    logging.info('post path: {path}'.format(path=postpath))

    posturl = "%s%s" % (SITE[:-1], postpath[:-5])
    logging.info('post url: {url}'.format(url=posturl))
    # Feed
    feed_path = '%s/%s' % (site_root, FEEDATOMNOM)
    logging.info('feed path: {path}'.format(path=feed_path))
    # Site Home Page
    home_path = '%s/%s' % (site_root, 'index.html')
    logging.info('home_path: {path}'.format(path=home_path))
    # Monthly index
    monthabspath = os.path.dirname(os.path.dirname(abspathpost))
    logging.info('month absolute path: {path}'.format(path=monthabspath))
    month_index_path = monthabspath + "/index.html"
    logging.info('month index path: {path}'.format(path=month_index_path))
    # *** END PATH CONFIGURATIONS ***

    # *** BACKUPS ***
    # preparing places for backup
    backup_path = '/tmp/lagrange'
    if not os.path.isdir(backup_path):
        os.mkdir(backup_path)
    feed_path_bkp = '%s/%s' % (backup_path, FEEDATOMNOM)
    shutil.copy(feed_path, feed_path_bkp)

    # *** BLOG POST INITIALIZATION ***
    post = Post(absolute_path=abspathpost)
    # Extracting Post Information
    title = post.title
    created = post.created_date
    modified = post.modified_date
    content = post.article

    # logging
    logging.info("TITLE: {}".format(title))
    logging.info("CREATED: {}".format(created))
    logging.info("MODIFIED: {}".format(modified))

    #
    date_now = helper.rfc3339_to_datetime(modified)

    # INDEX MARKUP
    new_entry_html = createindexmarkup(postpath[:-5], created, title)

    # MONTHLY INDEX CREATION
    # Create the monthly index if it doesn't exist yet
    # Happen once a month
    if not os.path.isfile(month_index_path):
        indexes.create_monthly_index(
            new_entry_html,
            month_index_path,
            date_now)
    else:
        # TOFIX: updating the monthly index
        # UPDATE THE MONTHLY INDEX
        if not dryrun:
            print('WE should write to the index')
            print(new_entry_html)
            # Return a dictionary of updated entries
            entries = indexes.update_monthly_index(new_entry_html, month_index_path)
            # TODO: Save as html
        else:
            print('TODO: Fix the update_monthly_index: update_monthly_index')
            print(('-' * 80))
            print(new_entry_html)

    # FEED ENTRY MARKUP
    # We compute the tagid using the creation date of the post
    created_dt = helper.rfc3339_to_datetime(created)
    created_iso = helper.convert_date(created_dt, 'iso')
    tagid = helper.create_tagid(posturl, created_iso)
    # UPDATING FEED
    feedentry_data = {'url': posturl,
                      'tagid': tagid,
                      'title': title,
                      'created': created,
                      'modified': helper.convert_date(date_now, 'rfc3339'),
                      'content': content}
    feedentry = feed.makefeedentry(feedentry_data)
    feed_content = feed.update_feed(feedentry, feed_path_bkp)

    # SAVE ATOM FEED
    if feed_content:
        if not dryrun:
            with open(feed_path, 'w') as feedbkp:
                feedbkp.write(feed_content.decode('utf-8'))
        else:
            print('TESTING: feedbkp.write(feed_content)')


if __name__ == "__main__":
    main()

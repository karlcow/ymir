#!/usr/bin/env python2.7
# encoding: utf-8
"""Helpers for the code.

Created by Karl Dubost on 2014-12-01.
Copyright (c) 2014 Grange. All rights reserved.
see LICENSE.TXT
"""

import locale
import logging
import os
import urllib.parse

from lxml import etree
from lxml.html import html5parser


ROOT = '/Users/karl/Sites/la-grange.net/'
WEB = 'http://lagrange.test.site/'
GRANGE = 'http://www.la-grange.net/'
BLOGPOST_LIST_PATH = '2014/12/01/grange-blogpost.uri'
BLOGPOST_LIST_URI = os.path.join(ROOT, BLOGPOST_LIST_PATH)


def convert_date(date_time, format=""):
    """Compute date in different date string formats."""
    # date in French please
    my_locale = "fr_FR"
    locale.setlocale(locale.LC_ALL, my_locale)
    if format == "rfc3339":
        return date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    elif format == "iso":
        return date_time.strftime("%Y-%m-%d")
    elif format == "path":
        return date_time.strftime("%Y/%m/%d")
    elif format == "humain":
        # remove the leading 0 of the date
        dategeek = date_time.strftime("%d %B %Y")
        if dategeek.startswith('0'):
            dategeek = dategeek.lstrip('0')
        return dategeek
    elif format == "humainlong":
        # Remove the leading 0
        # And add the day of the week
        # "Vendredi "+ "3 février 2012"
        dategeek = date_time.strftime("%d %B %Y")
        if dategeek.startswith('0'):
            dategeek = dategeek.lstrip('0')
        return date_time.strftime("%A ") + dategeek
    else:
        logging.error("date format is wrong. Check convert_date.")
        return None


def parse_raw_post(raw_post_path):
    """Given a path, parse an html file."""
    doc = html5parser.parse(raw_post_path).getroot()
    logging.info("parserrawpost: HTML document parsed")
    return doc


def parse_feed(feed_path):
    """Given the feed path, return a <type 'lxml.etree._Element'>."""
    parser = etree.XMLParser(ns_clean=True)
    with open(feed_path, 'r') as source:
        feed_tree = etree.parse(source, parser)
    logging.info("parse_feed: Feed has been parsed")
    return feed_tree


def create_tagid(post_url, iso_date):
    """Create a unide tagid for a given blog post.

    Example: tag:la-grange.net,2012-01-24:2012/01/24/silence
    """
    url_parts = urllib.parse.urlsplit(post_url)
    domain = url_parts.hostname
    # In la-grange case , we remove the www.
    # This might break elsewhere.
    domain = domain.lstrip('www.')
    path = url_parts.path.lstrip('/')
    tagid = 'tag:{domain},{iso_date}:{path}'.format(
        domain=domain,
        iso_date=iso_date,
        path=path)
    return tagid


def find_root(directory, token):
    """Find the root of a directory tree based on a token."""
    # Make sure we have a full path instead of a relative path
    if directory.startswith('.'):
        directory = os.path.realpath(directory)
    print(directory)
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
    return directory

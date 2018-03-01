#!/usr/bin/env python
# encoding: utf-8
"""
Parsing Module.

Created by Karl Dubost on 2018-03-01.
Copyright (c) 2018 Grange. All rights reserved.
see LICENSE.TXT
"""

import ConfigParser
import logging
import sys

from lxml import etree
from lxml.html import html5parser


config = ConfigParser.ConfigParser()
config.read('ymir/blog.cfg')

HTMLNS = config.get('constants', 'htmlns')


def parse_html_post(blogpost_path):
    """Given a path, parse an html file."""
    doc = html5parser.parse(blogpost_path).getroot()
    logging.info("HTML document parsed")
    return doc


def get_title(doc):
    """Return a list of markup and text being the title of the document."""
    target = '//{%s}h1[text()]' % HTMLNS
    findtitle = etree.ETXPath(target)
    if not findtitle(doc):
        sys.exit("ERROR: The document has no title")
    title = findtitle(doc)[0]
    titletext = etree.tostring(title, encoding="utf-8", method="text")
    titletext = titletext.strip()
    return titletext.decode('utf-8')

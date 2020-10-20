#!/usr/bin/env python
# encoding: utf-8
"""
Parses and updates indexes files.

Created by Karl Dubost on 2018-03-25.
Copyright (c) 2018 Grange. All rights reserved.
see LICENSE.TXT
"""

import datetime
import logging
import os
import string
import sys

import lxml.html
from lxml import etree

from ymir.utils import helper
from ymir.utils import parsing
from ymir.ymir import createindexmarkup


ROOT = '/Users/karl/Sites/la-grange.net'
CODEPATH = os.path.dirname(sys.argv[0])
TEMPLATEDIR = CODEPATH + "/../templates/"
DATENOW = datetime.datetime.today()


def create_monthly_index(entry_index, month_index_path, date_obj,
                         first_time=False):
    """Create a monthly index when it doesn't exist."""
    msg = "Do not forget to update /map with your tiny hands"
    logging.info("%s" % (msg))
    # Generate the html
    month_markup = month_index(entry_index, date_obj)
    return month_markup


def month_index(entry_index, date_obj):
    """Generate the markup for the month index."""
    # TODO: refactor the templating parts
    template_path = f'{ROOT}/2019/12/04/month_index_tmpl.html'
    with open(template_path, 'r') as source:
        t = string.Template(source.read())
        datestring = helper.convert_date(date_obj, 'iso')
        datehumain = helper.convert_date(date_obj, 'humain')
        # to get month, we split in 3 the human date and take the second
        # argument
        datemois = datehumain.split(' ')[1]
        tmpl_data = {
            'isodateshort': datestring,
            'month': datemois,
            'year': datestring[:4],
            'humandate': datehumain,
            'firstentry': entry_index
        }
        month_markup = t.substitute(tmpl_data)
    return month_markup


def update_monthly_index(new_entry_html, month_index_path):
    """Update the HTML Annual index with the feedendry.

    new_entry: str
        <li>etc…</li>
    month_index_path: str
        /2020/08/01/something.html
    """
    month_index = parsing.parse_xhtml_post(month_index_path)
    # Get a list of dictionaries for entries
    month_xpath = "//section[@id='month-index']/ul/li"
    entries = entries_as_dict(month_index, month_xpath)
    # Convert html entry to dict
    new_entry_xml = helper.make_xml(new_entry_html)
    new_entry = to_entry_dict(new_entry_xml)
    # Add the new entry to the list of entries
    update_entries(entries, new_entry)
    return entries


def update_entries(entries, new_entry):
    """Adds the new_entry to the entries.

    1. If new_entry URL is already in there, do not add to the list.
    2. It sorts the list according to the created date.
    """
    if not any(d['created'] == new_entry['created'] for d in entries):
        entries.append(new_entry)
    entries = sorted(entries, key=lambda k: k['created'])
    return entries


def entries_as_dict(document, xpath):
    """Convert index xml list to list of dictionaries."""
    # Search path
    findentrylist = etree.ETXPath(xpath)
    # Extract data
    entries_xml = findentrylist(document)
    entries = [to_entry_dict(entry_index_xml)
               for entry_index_xml in entries_xml]
    return entries


def to_entry_dict(entry_index_xml):
    """Convert an XML entry index into a dictionary."""
    # Search paths
    find_href = etree.ETXPath("a/@href")
    find_short_date = etree.ETXPath("time/text()")
    find_created = etree.ETXPath("time/@datetime")
    find_title = etree.ETXPath("a/text()")
    # extract data
    entry_index = {
        'created': find_created(entry_index_xml)[0],
        'iso_short_date': find_short_date(entry_index_xml)[0],
        'path': find_href(entry_index_xml)[0],
        'title': find_title(entry_index_xml)[0],
    }
    return entry_index

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
from ymir.ymir import createindexmarkup


ROOT = '/Users/karl/Sites/la-grange.net'
CODEPATH = os.path.dirname(sys.argv[0])
TEMPLATEDIR = CODEPATH + "/../templates/"
DATENOW = datetime.datetime.today()


def create_monthly_index(entry_index, month_index_path, date_obj):
    """Create a monthly index when it doesn't exist."""
    msg = "Do not forget to update /map with your tiny hands"
    logging.info("%s" % (msg))
    # Generate the html
    month_markup = month_index(entry_index, date_obj)
    # Save the file
    with open(month_index_path, 'w') as month_index:
        month_index.write(month_markup)


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
        print(tmpl_data)
        month_markup = t.substitute(tmpl_data)
    return month_markup


def update_monthly_index(entry_index, month_index_path):
    """Update the HTML Annual index with the feedendry.

    entry_index: str
        <li>etc…</li>
    month_index_path: str
        /2020/08/01/something.html
    """
    try:
        parsed_month = lxml.html.parse(month_index_path)
    except OSError as err:
        logging.ERROR(f"Monthly Index not found: {err}")
    else:
        month_index = parsed_month.getroot()
    entry_index_xml = helper.make_xml(entry_index)
    # Search path
    findentrylist = etree.ETXPath("//section[@id='month-index']/ul/li")
    # Extract data
    entries_xml = findentrylist(month_index)
    entries = [to_entry_dict(entry_index_xml)
               for entry_index_xml in entries_xml]
    # TODO: Convert to an html template.
    # TODO: Check if the entry already exist
    # TODO: Sort list based on date.
    print(entries)
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

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

import lxml
from lxml import etree

from . import helper

CODEPATH = os.path.dirname(sys.argv[0])
TEMPLATEDIR = CODEPATH + "/../templates/"
DATENOW = datetime.datetime.today()


def createmonthlyindex(indexmarkup, monthindexpath):
    """Create a monthly index when it doesn't exist."""
    # Code ici pour lire un fichier avec des variables
    # substituer les variables par les valeurs du mois
    # sauver le fichier au bon endroit
    msg = "Do not forget to update /map with your tiny hands"
    logging.info("%s" % (msg))

    with open(TEMPLATEDIR + 'index-mois.html', 'r') as source:
        t = string.Template(source.read())
        datestring = helper.convert_date(DATENOW, 'iso')
        datehumain = helper.convert_date(DATENOW, 'humain')
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


def updatemonthlyindex(indexmarkup, monthindexpath):
    """Update the HTML Annual index with the feedendry."""
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
        print(("ENTRY: ", created_entry, " TO ", created_ref))
        if href_entry == href_ref:
            print(('same uri', href_entry))
            # we check the date
            # we check the title
            # if changed replace
        else:
            pass

#!/usr/bin/env python2.7
# encoding: utf-8
"""Helpers for the code.

Created by Karl Dubost on 2014-12-01.
Copyright (c) 2014 Grange. All rights reserved.
see LICENSE.TXT
"""

import locale
import os
import sys


ROOT = '/Users/karl/Sites/la-grange.net/'
WEB = 'http://lagrange.test.site/'
GRANGE = 'http://www.la-grange.net/'
BLOGPOST_LIST_PATH = '2014/12/01/grange-blogpost.uri'
BLOGPOST_LIST_URI = os.path.join(ROOT, BLOGPOST_LIST_PATH)


def nowdate(date_time, format=""):
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
        print("wrong format")
        sys.exit(1)

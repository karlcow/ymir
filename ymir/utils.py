#!/usr/bin/env python2.7
# encoding: utf-8
'''
utils.py

Created by Karl Dubost on 2014-12-01.
Copyright (c) 2014 Grange. All rights reserved.
see LICENSE.TXT
'''

import os
import urllib2
import urlparse
import re

ROOT = '/Users/karl/Sites/la-grange.net/'
WEB = 'http://lagrange.test.site/'
GRANGE = 'http://www.la-grange.net/'
BLOGPOST_LIST_PATH = '2014/12/01/grange-blogpost.uri'
BLOGPOST_LIST_URI = os.path.join(ROOT, BLOGPOST_LIST_PATH)


def extract_title(text):
    '''Extract the title from La Grange.

    There are 3 possible patterns:
    * Karl - 2001-12-02 - Au revoir Normandie, weblog: script, Yves, Steph
      Karl - \d{4}-\d{2}-\d{2} - (.*)
    * La fille d'Ipanema - 2002-12-02 - Carnet Web Karl
      (.*) - \d{4}-\d{2}-\d{2} - Carnet Web Karl
    * Un long voyage - Carnets de La Grange
      (.*) - Carnets de La Grange
    '''
    # List of patterns
    pattern0 = re.compile('<title>(.*)</title>', re.IGNORECASE)
    title_patterns = [re.compile('Karl - \d{4}-\d{2}-\d{2} - (.*)'),
                      re.compile('(.*) - \d{4}-\d{2}-\d{2} - Carnet Web Karl'),
                      re.compile('(.*) - Carnets de La Grange'),
                      re.compile('(.*) - Carnets Web de La Grange')]
    TITLE = False
    TITLE_MATCH = False
    title = None
    title_line = None
    if not TITLE:
        for htmlline in text:
            line = htmlline.strip()
            if pattern0.match(line):
                TITLE = True
                html_title = pattern0.match(line).group(0)
                title_line = html_title[7:-8]
        for pattern in title_patterns:
            if pattern.match(title_line) and not TITLE_MATCH:
                TITLE_MATCH = True
                title = pattern.match(title_line).group(1)
    return title


def on_this_day(uri_list, month='01', day='01'):
    '''List all the blog posts at this date.'''
    blogposts = []
    onthisday_list = {}
    pattern = '{0}/{1}'.format(month, day)
    with open(uri_list, 'r') as source:
        text = source.read()
    blogposts = text.split('\n')
    for path in blogposts:
        if path[6:11] == pattern:
            uri = urlparse.urljoin(WEB, path)
            try:
                resp = urllib2.urlopen(uri)
            except urllib2.URLError, e:
                if e.code == 404:
                    break
            else:
                # 200
                text = resp.read().split('\n')
            title = extract_title(text)
            onthisday_list[urlparse.urljoin(GRANGE, path)] = title
    return onthisday_list
onthisday_list = on_this_day(BLOGPOST_LIST_URI, '02', '02')
print onthisday_list
for uri in onthisday_list.iterkeys():
    print '''* {0}
  {1}'''.format(onthisday_list[uri], uri)

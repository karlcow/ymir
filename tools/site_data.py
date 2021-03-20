#!/usr/bin/env python
# encoding: utf-8
"""
Parses and updates indexes files.

Created by Karl Dubost on 2020-10-31
see LICENSE.TXT
"""

from bs4 import BeautifulSoup
import httpx
from pathlib import Path
import re

webpages = []
sitemap_path = 'https://www.la-grange.net/map'


def get_charset(url):
    """Extract HTTP and HTML Charset.

    The HTML Charset has two cases:
    <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
    OR
    <meta charset="utf-8">
    """
    html_charset = None
    http_charset = None
    data = make_request(url)
    html_doc = parse_html(data.text)
    # HTTP Charset
    http_charset = data.charset_encoding
    # HTML Charset
    meta = html_doc.find_all(
        attrs={"http-equiv": re.compile(r'content-type', re.I)})
    if meta:
        html_charset = meta[0]['content'].split('=')[1]

    return html_charset, http_charset


def parse_html(html_text):
    return BeautifulSoup(html_text, 'html.parser')


def make_request(url):
    headers = {'User-Agent': 'KarlScrap/1.0'}
    return httpx.get(url, headers=headers)


def extract_urls(url, css_path):
    data = make_request(url)
    html_doc = parse_html(data.text)
    anchors = html_doc.select(css_path)
    links = [f'https://www.la-grange.net{anchor.get("href")}'
             for anchor in anchors]
    return links


# year_indexes = extract_urls(sitemap_path, 'table th > a')
# for year_index in year_indexes:
#     webpages.extend(extract_urls(year_index, '.month ul li a'))

# webpage = 'https://www.la-grange.net/2000/05/01'
webpage = 'https://www.la-grange.net/2020/10/31/effleurer'
html_charset, http_charset = get_charset(webpage)
print(f'HTML: {html_charset}\nHTTP: {http_charset}')
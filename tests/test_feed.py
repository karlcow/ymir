#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main code test
see LICENSE.TXT
"""

from io import BytesIO
import os
import unittest

from lxml import etree
import pytest

from tests.utils import make_xml
from ymir.utils import feed



class TestFeed(unittest.TestCase):
    """Test the main code."""

    def setUp(self):
        """Set up the tests."""
        self.maxDiff = None
        pass

    def tearDown(self):
        """Tear down the tests."""
        pass


    def test_makefeedentry(self):
        """Creating feed entry"""
        feedentry_data = {
            'url': 'http://example.org/somewhere',
            'tagid': 'example.org',
            'title': 'title',
            'created': 'date',
            'modified': 'date',
            'content': make_xml(b'<article>content</article>')}
        expected = make_xml(
            b'<entry xmlns="http://www.w3.org/2005/Atom">'
            b'<id>example.org</id><link rel="alternate" type="text/html" '
            b'href="http://example.org/somewhere"/><title>title</title>'
            b'<published>date</published><updated>date</updated><content '
            b'type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">'
            b'<article>content</article></div></content><link rel="license" '
            b'href="http://creativecommons.org/licenses/by/2.0/fr/"/></entry>')
        actual = etree.tostring(
            feed.makefeedentry(feedentry_data), encoding='unicode')
        expected = etree.tostring(expected, encoding='unicode')
        assert actual == expected

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

from ymir.utils import feed

FIXTURE_DIR = './tests/fixtures/'

class TestFeed(unittest.TestCase):
    """Test the main code."""

    def read_fixture(self, fixture_file):
        """Read the fixture for tests."""
        fixture_path = os.path.abspath(os.path.join(FIXTURE_DIR, fixture_file))
        return parsing.parse_html_post(fixture_path)

    def make_xml(self, text):
        """Convert a string as an etree Element."""
        parser = etree.XMLParser(remove_blank_text=True)
        xml_fragment = etree.parse(BytesIO(text), parser)
        return xml_fragment.getroot()

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
            'content': self.make_xml(b'<article>content</article>')}
        expected = self.make_xml(
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

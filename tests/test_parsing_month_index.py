#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parsing Blog Posts Unit Tests.

see LICENSE.TXT
"""

from io import BytesIO
import os
import unittest

from lxml import etree
import pytest

from ymir.utils import parsing

FIXTURE_DIR = './tests/fixtures/'

EXPECTED_MONTH_LIST = [
    {'created': '2018-11-11T11:52:44+09:00',
     'uri': '/2018/11/11/tancarville',
     'title': 'Le séchoir Tancarville'},
    {'created': '2018-11-11T16:18:22+09:00',
     'uri': '/2018/11/11/archive-perenne',
     'title': "Fragilité économique de l'archive pérenne"},
    {'created': '2018-11-12T16:57:27+09:00',
     'uri': '/2018/11/12/automne-enfoui',
     'title': 'Automne enfoui'}, ]


class TestYmirParsingMonth(unittest.TestCase):
    """Test the parsing rules for monthly index."""

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

    def test_get_title(self):
        """Test the extraction of title."""
        doc = self.read_fixture('month-index.html')
        actual = parsing.get_title(doc)
        expected = 'Archives novembre 2018'
        self.assertEqual(expected, actual)
        self.assertEqual(type(actual), str)

    def test_extract_month_list(self):
        """Extract the html fragment from monthly index."""
        doc = self.read_fixture('month-index-simple.html')
        content = parsing.get_html_month_list(doc)
        self.assertEqual(len(content), 2)
        actual = ''.join([etree.tostring(item, encoding='unicode')
                          for item in content])
        expected = '<html:li xmlns:html="http://www.w3.org/1999/xhtml"><html:time class="created" datetime="2018-11-11T11:52:44+09:00">2018-11-11</html:time> : <html:a href="/2018/11/11/tancarville">Le séchoir Tancarville</html:a></html:li>\n<html:li xmlns:html="http://www.w3.org/1999/xhtml"><html:time class="created" datetime="2018-11-11T16:18:22+09:00">2018-11-11</html:time> : <html:a href="/2018/11/11/archive-perenne">Fragilité économique de l\'archive pérenne</html:a></html:li>\n'  # noqa
        assert actual == expected

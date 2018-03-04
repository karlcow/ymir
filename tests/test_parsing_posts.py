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

from ymir.utils import parsing

FIXTURE_DIR = './tests/fixtures/'


class TestYmirParsing(unittest.TestCase):
    """Test the parsing rules for the blog posts."""

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
        pass

    def tearDown(self):
        """Tear down the tests."""
        pass

    def test_get_title(self):
        """Test the extraction of the title."""
        title_tests = [
            (u'What about 森野?', 'title-utf8.html'),
            (u'Simple title', 'title-markup.html'),
            (u'Simple title', 'title-space.html'),
            (u'Simple title', 'title-simple.html')]
        for expected, filename in title_tests:
            doc = self.read_fixture(filename)
            actual = parsing.get_title(doc)
            self.assertEqual(expected, actual)

    def test_get_date(self):
        """Test the extraction of the date."""
        doc = self.read_fixture('date-created-modified.html')
        created = parsing.get_date(doc, 'created')
        self.assertEqual('2018-03-01T15:54:34+01:00', created)
        modified = parsing.get_date(doc, 'modified')
        self.assertEqual('2018-03-02T15:54:34+01:00', modified)
        with self.assertRaises(ValueError) as ctx:
            parsing.get_date(doc, 'foobar')
        self.assertEqual(
            ctx.exception.message,
            "date type must be one of ['modified', 'created']")

    def test_get_content(self):
        """Test the extraction of the content."""
        # normal case
        expected = '<html:article xmlns:html="http://www.w3.org/1999/xhtml"><html:p>This is content: &#28961;</html:p></html:article>'  # noqa
        doc = self.read_fixture('content-simple.html')
        content = parsing.get_content(doc)
        self.assertEqual(
            etree.tostring(self.make_xml(expected), with_tail=False),
            etree.tostring(content).replace('\n', ''))
        # no header in the content
        expected = '<html:article xmlns:html="http://www.w3.org/1999/xhtml"><html:p>content without header</html:p></html:article>'  # noqa
        doc = self.read_fixture('content-no-header.html')
        content = parsing.get_content(doc)
        self.assertEqual(
            etree.tostring(self.make_xml(expected), with_tail=False),
            etree.tostring(content).replace('\n', ''))
        # there is no article
        doc = self.read_fixture('content-none.html')
        with self.assertRaises(IndexError) as ctx:
            parsing.get_content(doc)
        self.assertEqual(
            ctx.exception.message,
            "Ooops. No article.")

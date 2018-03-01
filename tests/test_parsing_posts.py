#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parsing Blog Posts Unit Tests.

see LICENSE.TXT
"""

import os
import unittest

from ymir.utils import parsing

FIXTURE_DIR = './tests/fixtures/'


class TestYmirParsing(unittest.TestCase):
    """Test the parsing rules for the blog posts."""

    def read_fixture(self, fixture_file):
        """Read the fixture for tests."""
        fixture_path = os.path.abspath(os.path.join(FIXTURE_DIR, fixture_file))
        return parsing.parse_html_post(fixture_path)

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
            (u'Simple title', 'title-simple.html')]
        for expected, filename in title_tests:
            doc = self.read_fixture(filename)
            actual = parsing.get_title(doc)
            self.assertEqual(expected, actual)

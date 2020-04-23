#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test helpers functions for Ymir.

see LICENSE.TXT
"""

import datetime
import os
import unittest

from lxml import etree

from ymir.utils import helper

FIXTURE_DIR = './tests/fixtures/'


class TestYmirHelper(unittest.TestCase):
    """Test the helpers for Ymir."""

    def setUp(self):
        """Set up the tests."""
        pass

    def tearDown(self):
        """Tear down the tests."""
        pass

    def test_convert_date(self):
        """Check the different date conversions."""
        # 2 April 2000  08:09:10.0
        test_date = datetime.datetime(2000, 4, 2, 8, 9, 10, 0)
        self.assertEqual(
            helper.convert_date(test_date, 'rfc3339'),
            '2000-04-02T08:09:10Z')
        self.assertEqual(
            helper.convert_date(test_date, 'iso'),
            '2000-04-02')
        self.assertEqual(
            helper.convert_date(test_date, 'path'),
            '2000/04/02')
        self.assertEqual(
            helper.convert_date(test_date, 'humain'),
            '2 avril 2000')
        self.assertEqual(
            helper.convert_date(test_date, 'humainlong'),
            'Dimanche 2 avril 2000')
        self.assertIsNone(helper.convert_date(test_date, 'foobar'))

    def test_rfc3339_to_datetime_with_Z(self):
        """Test date conversion."""
        date_in = '2014-04-04T23:59:00Z'
        actual = helper.rfc3339_to_datetime(date_in)
        expected = datetime.datetime(2014, 4, 4, 23, 59)
        assert actual == expected

    def test_rfc3339_to_datetime_without_Z(self):
        """Test date conversion."""
        # tz + 9 hours
        date_in = '2014-04-04T23:59:00+09:00'
        actual = helper.rfc3339_to_datetime(date_in)
        expected = datetime.datetime(2014, 4, 4, 14, 59)
        assert actual == expected
        # tz - 9 hours
        date_in = '2014-04-04T23:59:00-09:00'
        actual = helper.rfc3339_to_datetime(date_in)
        expected = datetime.datetime(2014, 4, 5, 8, 59)
        assert actual == expected

    def test_create_tagid(self):
        """Test tagid creation."""
        expected = 'tag:la-grange.net,2012-01-24:2012/01/24/silence'
        post_url = 'http://www.la-grange.net/2012/01/24/silence'
        iso_date = '2012-01-24'
        actual = helper.create_tagid(post_url, iso_date)
        self.assertEqual(actual, expected)

    def test_parse_raw_post(self):
        """Test raw post parsing"""
        fixture_file = 'content-simple.html'
        fixture_path = os.path.abspath(os.path.join(FIXTURE_DIR, fixture_file))
        actual = helper.parse_raw_post(fixture_path)
        actual_normalized = etree.tostring(actual, encoding='unicode').replace('\n', '')  # noqa
        expected = (
            '<html:html xmlns:html="http://www.w3.org/1999/xhtml" '
            'lang="fr"><html:head><html:meta charset="utf-8"/>'
            '</html:head><html:body>'
            '<html:header>'
            '<html:h1>Simple title</html:h1>'
            '</html:header>'
            '<html:article>'
            '<html:p>This is content: 無</html:p>'
            '</html:article>'
            '</html:body></html:html>')
        assert type(actual).__name__ == '_Element'
        assert  actual_normalized == expected

    def test_parse_feed(self):
        """Test feed parsing"""
        fixture_file = 'feed.atom'
        fixture_path = os.path.abspath(os.path.join(FIXTURE_DIR, fixture_file))
        actual = helper.parse_feed(fixture_path)
        actual_normalized = etree.tostring(actual, encoding='unicode').replace('\n', '')  # noqa
        expected = (
            '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="fr">'
            '<title>Carnets de La Grange</title>'
            "<subtitle>Chroniques d'un poète urbain</subtitle>"
            '<id>tag:la-grange.net,2000-04-12:karl</id>'
            '  <updated>2020-04-21T14:59:59Z</updated>'
            '<link href="http://www.la-grange.net/feed.atom" rel="self"'
            ' type="application/atom+xml"/>'
            '<link href="http://www.la-grange.net/" rel="alternate" '
            'type="application/xhtml+xml"/>'
            '<link href="http://creativecommons.org/licenses/by/2.0/fr/" '
            'rel="license"/><icon>http://www.la-grange.net/favicon.png</icon>'
            '<author>    <name>Karl Dubost</name>    '
            '<uri>http://www.la-grange.net/karl/</uri></author>'
            '<entry>    '
            '<id>tag:la-grange.net,2020-04-21:2020/04/21/absence</id>    '
            '<link rel="alternate" type="text/html" '
            'href="http://www.la-grange.net/2020/04/21/absence"/>'
            '    <title>absences</title>'
            '    <published>2020-04-21T23:59:59+09:00</published>'
            '    <updated>2020-04-21T14:59:59Z</updated>'
            '    <content type="xhtml">'
            '        <div xmlns="http://www.w3.org/1999/xhtml">'
            '            <article class="item post">un billet</article>'
            '        </div>'
            '    </content>'
            '    <link rel="license"'
            ' href="http://creativecommons.org/licenses/by/2.0/fr/"/></entry>'
            '</feed>')
        assert type(actual).__name__ == '_ElementTree'
        assert  actual_normalized == expected

    def test_find_root(self):
        """test the root finding."""
        post_directory = './tests/fixtures/fake_tree/2020/01/01'
        actual = helper.find_root(post_directory, 'root_token')
        assert actual.endswith('tests/fixtures/fake_tree')
        post_directory = './tests/fixtures/'
        actual = helper.find_root(post_directory, 'root_token')
        assert actual == None
        post_directory = './tests/fixtures/2020/02'
        actual = helper.find_root(post_directory, 'root_token')
        assert actual == None

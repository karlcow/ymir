#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test helpers functions for Ymir.

see LICENSE.TXT
"""

import datetime
import unittest

from ymir.utils import helper


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

    def test_create_tagid(self):
        """Test tagid creation."""
        expected = 'tag:la-grange.net,2012-01-24:2012/01/24/silence'
        post_url = u'http://www.la-grange.net/2012/01/24/silence'
        iso_date = u'2012-01-24'
        actual = helper.create_tagid(post_url, iso_date)
        self.assertEqual(actual, expected)

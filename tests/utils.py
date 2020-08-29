#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main code test
see LICENSE.TXT
"""

import os
from io import BytesIO

from lxml import etree

from ymir.utils import parsing

FIXTURE_DIR = './tests/fixtures/'


def read_fixture(fixture_file):
    """Read the fixture for tests."""
    fixture_path = get_fixture_path(fixture_file)
    return parsing.parse_html_post(fixture_path)


def read_text_fixture(fixture_file):
    """Read the fixture for tests."""
    fixture_path = get_fixture_path(fixture_file)
    with open(fixture_path, 'r') as f:
        text = f.read()
    return text


def get_fixture_path(fixture_file):
    """Send the full fixture path."""
    return os.path.abspath(os.path.join(FIXTURE_DIR, fixture_file))


def make_xml(text):
    """Convert a string as an etree Element."""
    parser = etree.XMLParser(remove_blank_text=True)
    xml_fragment = etree.parse(BytesIO(text), parser)
    return xml_fragment.getroot()

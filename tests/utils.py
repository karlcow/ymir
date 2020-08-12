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
    fixture_path = os.path.abspath(os.path.join(FIXTURE_DIR, fixture_file))
    return parsing.parse_html_post(fixture_path)


def make_xml(text):
    """Convert a string as an etree Element."""
    parser = etree.XMLParser(remove_blank_text=True)
    xml_fragment = etree.parse(BytesIO(text), parser)
    return xml_fragment.getroot()

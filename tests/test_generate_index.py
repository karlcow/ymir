from datetime import datetime

import pytest

from tests.utils import get_fixture_path
from tests.utils import read_text_fixture
from ymir.utils import indexes
from ymir.utils import helper


def test_generate_monthly_placeholder():
    """Test the reading of templating and creation of the right markup."""
    entry_index = '<li><time class="created" datetime="2020-08-01T23:59:59+09:00">2020-08-01</time> : <a href="/location">titre</a></li>'  # noqa
    date = datetime(2020, 8, 1)
    expected = read_text_fixture('month_index_empty.html')
    assert indexes.month_index(entry_index, date) == expected


def test_update_monthly_index():
    """Test that the current file is being correctly updated."""
    entry_index = '<li><time class="created" datetime="2020-08-16T23:59:59+09:00">2020-08-16</time> : <a href="/2020/08/16/new_path">new post</a></li>'  # noqa
    month_index_path = get_fixture_path('month_index_to_update.html')
    expected_month = read_text_fixture('month_index_updated.html')
    actual_month = indexes.update_monthly_index(entry_index, month_index_path)
    # assert actual_month == expected_month
    assert actual_month == entries_list


def test_entry_index_to_dict():
    """Test the conversion from XML to dict structure for index entry."""
    entry_index = '<li><time class="created" datetime="2020-08-16T23:59:59+09:00">2020-08-16</time> : <a href="/2020/08/16/new_path">new post</a></li>'  # noqa
    entry_index_xml = helper.make_xml(entry_index)
    expected = {
        'created': '2020-08-16T23:59:59+09:00',
        'iso_short_date': '2020-08-16',
        'path': '/2020/08/16/new_path',
        'title': 'new post',
    }
    assert indexes.to_entry_dict(entry_index_xml) == expected


entries_list = [{'created': '2020-08-01T23:59:59+09:00', 'iso_short_date': '2020-08-01', 'path': '/2020/08/01/ocean', 'title': "en revenant de l'océan"}, {'created': '2020-08-02T23:59:59+09:00', 'iso_short_date': '2020-08-02', 'path': '/2020/08/02/pente', 'title': 'envie des pentes'}, {'created': '2020-08-03T23:59:59+09:00', 'iso_short_date': '2020-08-03', 'path': '/2020/08/03/baguette', 'title': 'baguette'}, {'created': '2020-08-04T23:59:59+09:00', 'iso_short_date': '2020-08-04', 'path': '/2020/08/04/tas', 'title': 'tas de photos'}, {'created': '2020-08-05T23:59:59+09:00', 'iso_short_date': '2020-08-05', 'path': '/2020/08/05/rouille', 'title': 'rouille'}, {'created': '2020-08-06T23:59:59+09:00', 'iso_short_date': '2020-08-06', 'path': '/2020/08/06/au-dessus', 'title': 'au dessus'}, {'created': '2020-08-07T23:59:59+09:00', 'iso_short_date': '2020-08-07', 'path': '/2020/08/07/bernard-stiegler', 'title': 'Bernard Stiegler'}, {'created': '2020-08-08T23:59:59+09:00', 'iso_short_date': '2020-08-08', 'path': '/2020/08/08/abandon', 'title': "possibilité de l'abandon"}, {'created': '2020-08-09T23:59:59+09:00', 'iso_short_date': '2020-08-09', 'path': '/2020/08/09/persil-chenille', 'title': 'persil'}, {'created': '2020-08-10T23:59:59+09:00', 'iso_short_date': '2020-08-10', 'path': '/2020/08/10/conditionnement', 'title': 'conditionnement'}, {'created': '2020-08-11T23:59:59+09:00', 'iso_short_date': '2020-08-11', 'path': '/2020/08/11/suspension', 'title': 'suspension'}, {'created': '2020-08-12T23:59:59+09:00', 'iso_short_date': '2020-08-12', 'path': '/2020/08/12/fascination', 'title': 'fascination'}, {'created': '2020-08-13T23:59:59+09:00', 'iso_short_date': '2020-08-13', 'path': '/2020/08/13/introspection', 'title': 'introspection'}, {'created': '2020-08-14T23:59:59+09:00', 'iso_short_date': '2020-08-14', 'path': '/2020/08/14/planifier', 'title': 'planifier'}, {'created': '2020-08-15T23:59:59+09:00', 'iso_short_date': '2020-08-15', 'path': '/2020/08/15/dilue', 'title': 'dilué'}]  # noqa
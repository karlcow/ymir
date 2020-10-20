from datetime import datetime

import pytest

from tests.utils import get_fixture_path
from tests.utils import read_text_fixture
from ymir.utils import indexes
from ymir.utils import helper
from ymir.utils import parsing

entries_list = [{'created': '2020-08-01T23:59:59+09:00', 'iso_short_date': '2020-08-01', 'path': '/2020/08/01/ocean', 'title': "en revenant de l'océan"}, {'created': '2020-08-02T23:59:59+09:00', 'iso_short_date': '2020-08-02', 'path': '/2020/08/02/pente', 'title': 'envie des pentes'}, {'created': '2020-08-03T23:59:59+09:00', 'iso_short_date': '2020-08-03', 'path': '/2020/08/03/baguette', 'title': 'baguette'}, {'created': '2020-08-04T23:59:59+09:00', 'iso_short_date': '2020-08-04', 'path': '/2020/08/04/tas', 'title': 'tas de photos'}, {'created': '2020-08-05T23:59:59+09:00', 'iso_short_date': '2020-08-05', 'path': '/2020/08/05/rouille', 'title': 'rouille'}, {'created': '2020-08-06T23:59:59+09:00', 'iso_short_date': '2020-08-06', 'path': '/2020/08/06/au-dessus', 'title': 'au dessus'}, {'created': '2020-08-07T23:59:59+09:00', 'iso_short_date': '2020-08-07', 'path': '/2020/08/07/bernard-stiegler', 'title': 'Bernard Stiegler'}, {'created': '2020-08-08T23:59:59+09:00', 'iso_short_date': '2020-08-08', 'path': '/2020/08/08/abandon', 'title': "possibilité de l'abandon"}, {'created': '2020-08-09T23:59:59+09:00', 'iso_short_date': '2020-08-09', 'path': '/2020/08/09/persil-chenille', 'title': 'persil'}, {'created': '2020-08-10T23:59:59+09:00', 'iso_short_date': '2020-08-10', 'path': '/2020/08/10/conditionnement', 'title': 'conditionnement'}, {'created': '2020-08-11T23:59:59+09:00', 'iso_short_date': '2020-08-11', 'path': '/2020/08/11/suspension', 'title': 'suspension'}, {'created': '2020-08-12T23:59:59+09:00', 'iso_short_date': '2020-08-12', 'path': '/2020/08/12/fascination', 'title': 'fascination'}, {'created': '2020-08-13T23:59:59+09:00', 'iso_short_date': '2020-08-13', 'path': '/2020/08/13/introspection', 'title': 'introspection'}, {'created': '2020-08-14T23:59:59+09:00', 'iso_short_date': '2020-08-14', 'path': '/2020/08/14/planifier', 'title': 'planifier'}, {'created': '2020-08-15T23:59:59+09:00', 'iso_short_date': '2020-08-15', 'path': '/2020/08/15/dilue', 'title': 'dilué'}, {'created': '2020-08-16T23:59:59+09:00', 'iso_short_date': '2020-08-16', 'path': '/2020/08/16/new_path', 'title': 'new post'}]  # noqa

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


def test_entries_as_dict_month():
    """Extract the entries from a markup file."""
    # For month index
    index_path = get_fixture_path('month-index.html')
    month_xpath = "//section[@id='month-index']/ul/li"
    index_markup = parsing.parse_xhtml_post(index_path)
    expected = [{'created': '2018-11-11T11:52:44+09:00', 'iso_short_date': '2018-11-11', 'path': '/2018/11/11/tancarville', 'title': 'Le séchoir Tancarville'}, {'created': '2018-11-11T16:18:22+09:00', 'iso_short_date': '2018-11-11', 'path': '/2018/11/11/archive-perenne', 'title': "Fragilité économique de l'archive pérenne"}, {'created': '2018-11-12T16:57:27+09:00', 'iso_short_date': '2018-11-12', 'path': '/2018/11/12/automne-enfoui', 'title': 'Automne enfoui'}]  # noqa
    assert expected == indexes.entries_as_dict(index_markup, month_xpath)


def test_entries_as_dict_year():
    """Extract the entries from a markup file."""
    # For annual index
    year_index_path = get_fixture_path('annual-index.html')
    year_xpath = "//section[@class='month index y2020 m10']/ul/li"
    year_index_markup = parsing.parse_xhtml_post(year_index_path)
    expected = [{'created': '2020-10-01T23:59:59+09:00', 'iso_short_date': '2020-10-01', 'path': '/2020/10/01/etoiles', 'title': 'sous les étoiles'}, {'created': '2020-10-02T23:59:59+09:00', 'iso_short_date': '2020-10-02', 'path': '/2020/10/02/arbres', 'title': 'arbres de kugenuma'}, {'created': '2020-10-03T23:59:59+09:00', 'iso_short_date': '2020-10-03', 'path': '/2020/10/03/jardin', 'title': 'entretiens de jardin'}, {'created': '2020-10-04T23:59:59+09:00', 'iso_short_date': '2020-10-04', 'path': '/2020/10/04/kandisky', 'title': 'chenille Kandinsky'}, {'created': '2020-10-05T23:59:59+09:00', 'iso_short_date': '2020-10-05', 'path': '/2020/10/05/humain', 'title': "chasser l'humain"}, {'created': '2020-10-06T23:59:59+09:00', 'iso_short_date': '2020-10-06', 'path': '/2020/10/06/peau', 'title': 'seconde peau'}, {'created': '2020-10-07T23:59:59+09:00', 'iso_short_date': '2020-10-07', 'path': '/2020/10/07/abysses', 'title': 'marcher les abysses'}, {'created': '2020-10-08T23:59:59+09:00', 'iso_short_date': '2020-10-08', 'path': '/2020/10/08/asperite', 'title': 'aspérités'}, {'created': '2020-10-09T23:59:59+09:00', 'iso_short_date': '2020-10-09', 'path': '/2020/10/09/neuf', 'title': 'neuf'}, {'created': '2020-10-10T23:59:59+09:00', 'iso_short_date': '2020-10-10', 'path': '/2020/10/10/entre-deux', 'title': 'entre deux'}, {'created': '2020-10-11T23:59:59+09:00', 'iso_short_date': '2020-10-11', 'path': '/2020/10/11/breche', 'title': 'brèche'}, {'created': '2020-10-12T23:59:59+09:00', 'iso_short_date': '2020-10-12', 'path': '/2020/10/12/extase', 'title': 'extase du doute'}, {'created': '2020-10-13T23:59:59+09:00', 'iso_short_date': '2020-10-13', 'path': '/2020/10/13/amer', 'title': 'amer'}, {'created': '2020-10-14T23:59:59+09:00', 'iso_short_date': '2020-10-14', 'path': '/2020/10/14/kaki', 'title': 'kaki'}, {'created': '2020-10-15T23:59:59+09:00', 'iso_short_date': '2020-10-15', 'path': '/2020/10/15/cote', 'title': 'quatre côtés'}, {'created': '2020-10-16T23:59:59+09:00', 'iso_short_date': '2020-10-16', 'path': '/2020/10/16/mains-sales', 'title': 'mains sales'}, {'created': '2020-10-17T23:59:59+09:00', 'iso_short_date': '2020-10-17', 'path': '/2020/10/17/reflet', 'title': 'reflet'}, {'created': '2020-10-18T23:59:59+09:00', 'iso_short_date': '2020-10-18', 'path': '/2020/10/18/tofu', 'title': 'lieu du tofu'}, {'created': '2020-10-19T23:59:59+09:00', 'iso_short_date': '2020-10-19', 'path': '/2020/10/19/fuji', 'title': 'Fuji'}]  # noqa
    print(indexes.entries_as_dict(year_index_markup, year_xpath))
    assert expected == indexes.entries_as_dict(year_index_markup, year_xpath)


def test_create_month_xpath_in_annual_index():
    """Given a month, create the relevant xpath to extract the month."""
    expected = "//section[@class='month index y2020 m10']/ul/li"
    assert expected == indexes.create_month_xpath(2020, 10)